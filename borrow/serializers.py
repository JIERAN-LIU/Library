import datetime

from django.utils import timezone
from rest_framework import serializers

from borrow.models import BorrowRecord
from common.constant import Constant


class BookActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id']


class BookFineSerializer(BookActionSerializer):
    class Meta(BookActionSerializer.Meta):
        fields = ['id', 'fine', 'pay_method', 'currency_symbol', 'fined_at']


class BorrowRecordSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField(read_only=True)
    reader_info = serializers.SerializerMethodField(read_only=True)
    has_overdue = serializers.SerializerMethodField(read_only=True)
    remain_days = serializers.SerializerMethodField(read_only=True)
    overdue_days = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_info', 'copy', 'reader', 'reader_info', 'borrowed_at', 'returned_at',
                  'renewed_at', 'has_returned', 'has_renewed', 'has_overdue', 'has_fined', 'fine', 'pay_method',
                  'currency_symbol', 'fined_at', 'remain_days', 'overdue_days']
        extra_kwargs = {
            'borrowed_at': {'read_only': True},
            'returned_at': {'read_only': True},
            'renewed_at': {'read_only': True},
            'fined_at': {'read_only': True},
            'has_returned': {'read_only': True},
            'has_renewed': {'read_only': True},
            'has_fined': {'read_only': True},
            'has_overdue': {'read_only': True},
            'fine': {'read_only': True},
            'pay_method': {'read_only': True},
            'currency_symbol': {'read_only': True},
            'book': {'write_only': True},
            'reader': {'write_only': True},
        }

    def get_overdue_days(self, obj: BorrowRecord):
        max_days = self.get_max_days(obj)
        now = timezone.now()
        delta = now - obj.borrowed_at
        return max(0, (delta - max_days).days.real)

    def get_has_overdue(self, obj):
        max_days = self.get_max_days(obj)
        delta = timezone.now() - obj.borrowed_at
        return delta >= max_days

    def get_remain_days(self, obj):
        if obj.has_returned:
            return 0
        max_days = self.get_max_days(obj)
        now = timezone.now()
        return max(0, (max_days - (now - obj.borrowed_at)).days.real)

    @staticmethod
    def get_max_days(obj) -> datetime.timedelta:
        max_days = Constant.MAX_BORROW_DAY
        if obj.has_renewed:
            max_days *= 2
        return datetime.timedelta(days=max_days)

    @staticmethod
    def get_book_info(obj):
        book = obj.book
        if not book:
            book = BorrowRecord.objects.get(id=obj.id).book
        return {'id': book.id, 'title': book.title, 'cover': book.cover} if book else {}

    @staticmethod
    def get_reader_info(obj):
        reader = obj.reader
        if not reader:
            reader = BorrowRecord.objects.get(id=obj.id).reader
        return {'id': reader.id, 'title': reader.nickname or reader.username, 'avatar': reader.avatar} if reader else {}
