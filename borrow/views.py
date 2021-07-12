from django.utils import timezone
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from book.models import BookCopy, Book
from borrow.models import BorrowRecord
from borrow.serializers import BorrowRecordSerializer, BookActionSerializer, BookFineSerializer
from common.constant import Constant
from common.views import LibraryViewSetMixin, BaseError


class BorrowRecordViewSet(LibraryViewSetMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    queryset = BorrowRecord.objects.all().order_by('-borrowed_at')
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        self.validate_copy(serializer)
        super(BorrowRecordViewSet, self).perform_create(serializer)
        update_copy(self.request, Constant.BOOK_COPY_STATUS_ON_BORROWING)

    @staticmethod
    def validate_copy(serializer):
        copy: BookCopy = serializer.validated_data['copy']
        if copy.status != Constant.BOOK_STATUS_AVAILABLE:
            raise BaseError("The copy is on borrowing")

    @staticmethod
    def validate_borrow_record(serializer):
        book: Book = serializer.validated_data['book']
        reader = serializer.validate_data['reader']
        records = BorrowRecord.objects.filter(book=book.id, reader=reader.id).filter(has_returned=False)
        if len(records):
            raise BaseError(detail="One book only is borrowed by same reader once at the same time")


class BookCopyReturnViewSet(LibraryViewSetMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = BorrowRecord.objects.all().order_by('-borrowed_at')
    serializer_class = BookActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        record: BorrowRecord = BorrowRecord.objects.get(id=self.get_pk())
        if record.has_returned:
            raise BaseError(detail="The copy is already returned")

        user = self.fill_user(serializer, 'update')
        serializer.save(has_returned=True, returned_at=timezone.now(), **user)
        update_copy(self.request, Constant.BOOK_STATUS_AVAILABLE, record.copy_id)


class BookCopyRenewViewSet(BookCopyReturnViewSet):

    def perform_update(self, serializer):
        record: BorrowRecord = BorrowRecord.objects.get(id=self.get_pk())
        if record.has_renewed or record.has_returned:
            raise BaseError(detail="The copy is already returned")
        user = self.fill_user(serializer, 'update')
        serializer.save(has_renewed=True, renewed_at=timezone.now(), **user)


class BookCopyFineViewSet(BookCopyReturnViewSet):
    serializer_class = BookFineSerializer

    def perform_update(self, serializer):
        record: BorrowRecord = BorrowRecord.objects.get(id=self.get_pk())
        serializer_borrow_record = BorrowRecordSerializer(record)
        if not serializer_borrow_record.data.get('has_overdue') or record.has_fined:
            raise BaseError(detail="The copy does not need  fine")
        user = self.fill_user(serializer, 'update')
        serializer.save(
            has_overdue=True,
            has_returned=True,
            returned_at=timezone.now(),
            has_fined=True,
            fined_at=timezone.now(),
            **user
        )
        update_copy(self.request, Constant.BOOK_STATUS_AVAILABLE, record.copy_id)


def update_copy(request, status, copy_id=None):
    copy_id = copy_id or request.data['copy'] or request.data['copy_id']
    copy = BookCopy.objects.get(id=copy_id)
    copy.status = status
    copy.save()
