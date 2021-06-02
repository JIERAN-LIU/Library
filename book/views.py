import random
#view
from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response

from book.models import Author, Book, Publisher, BookCopy
from book.serializers import AuthorSerializer, BookSerializer, PublisherSerializer, BookCopySerializer
from common.constant import Constant
from common.views import BaseModelViewSet


class BookViewSet(BaseModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        extra_infos = self.fill_user(serializer, 'create')
        extra_infos.update(self.gen_call_number())
        serializer.save(**extra_infos)
        self.save_copies(serializer)

    def filter_queryset(self, queryset):
        queryset = super(BookViewSet, self).filter_queryset(queryset)
        return queryset.exclude(status=Constant.BOOK_STATUS_DELETED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        copies_on_borrow = instance.copies.filter(status=Constant.BOOK_COPY_STATUS_ON_BORROWING)
        if len(copies_on_borrow):
            return Response(
                data={'detail': 'There are some copy on borrowing'},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance: Book):
        instance.status = Constant.BOOK_STATUS_DELETED
        instance.save()

    @staticmethod
    def save_copies(serializer):
        data = serializer.data
        if 'copies' not in data:
            return

        copies = data['copies']
        add_barcode_data = []
        barcode_list = gen_barcode(len(copies))
        for i, c in enumerate(copies):
            add_barcode_data.append({
                **c,
                'barcode': barcode_list[i]
            })
        serializer = BookCopySerializer(data=add_barcode_data, many=True)
        serializer.save(book_id=data['id'][0])

    def gen_call_number(self):
        """
        Generate Call number by Library of Congress Classification
        :return: call_number str
        """
        data = self.request.data
        subject = data['subject'][0]
        author_id = data['author'][0] or data['author_id'][0]
        publication_date = data['publication_date'][0].replace('-', '').replace('/', '')
        code = Constant.BOOK_SUBJECT_CODE[subject]
        author = Author.objects.get(id=author_id)
        ret = '{}{}.{}{}.{}'.format(code,
                                    str(random.randint(1, 9999)).ljust(4, '0'),
                                    author.name[0].upper(),
                                    str(random.randint(1, 999)).ljust(3, '0'),
                                    publication_date)
        return {'call_number': ret}


class AuthorViewSet(BaseModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class PublisherViewSet(BaseModelViewSet):
    queryset = Publisher.objects.all().order_by('name')
    serializer_class = PublisherSerializer


class BookCopyViewSet(BaseModelViewSet):
    queryset = BookCopy.objects.all().order_by('barcode')
    serializer_class = BookCopySerializer

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        book = query_params.get('book', None)
        if not book:
            return queryset[0:0]
        queryset = queryset.filter(book_id=book[0])
        return super(BookCopyViewSet, self).filter_queryset(queryset)

    def perform_create(self, serializer):
        extra_infos = self.fill_user(serializer, 'create')
        extra_infos['barcode'] = gen_barcode(1)[0]
        serializer.save(**extra_infos)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == Constant.BOOK_COPY_STATUS_ON_BORROWING:
            return Response(
                data={'detail': 'There are some copy on borrowing'},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.status = Constant.BOOK_STATUS_DELETED
        instance.save()


def gen_barcode(num):
    """
    Generate book copy's barcode
    :param num: number of book copy
    :return: a barcode list which size is save as num
    """
    ret = []
    copy_cnt = BookCopy.objects.count()
    if not copy_cnt:
        max_barcode = '1000000001'
    else:
        max_barcode = BookCopy.objects.aggregate(Max('barcode'))['barcode__max']
    max_barcode_int = int(max_barcode)
    for i in range(num):
        max_barcode_int += 1
        ret.append(str(max_barcode))
    return ret
