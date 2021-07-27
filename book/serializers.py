from django.db.models import Max
from rest_framework import serializers

from book.models import Book, Publisher, Author, BookCopy
from common.constant import Constant


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'email', 'logo', 'site']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'gender', 'nation', 'avatar', 'profile', 'birthday', 'died_at']


class BookCopySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BookCopy
        fields = ['id', 'barcode', 'status', 'location', 'section', 'media_type', 'book']
        extra_kwargs = {
            'barcode': {'read_only': True},
            'status': {'read_only': True},
            'book': {'required': False},
        }


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']


class BookSerializer(serializers.ModelSerializer):
    publisher_info = serializers.SerializerMethodField(read_only=True)
    authors_info = serializers.SerializerMethodField(read_only=True)
    copies = BookCopySerializer(many=True, write_only=True, required=False)
    available_number = serializers.SerializerMethodField(read_only=True)
    comment_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'language', 'subject', 'cover', 'description', 'isbn_10', 'isbn_13', 'publisher',
                  'publisher_info', 'publication_date', 'call_number', 'authors', 'authors_info', 'toc', 'price',
                  'print_length', 'binding', 'copies', 'comment_summary', 'available_number']

        extra_kwargs = {
            'publisher': {'write_only': True},
            'authors': {'write_only': True},
            'call_number': {'read_only': True},
        }

    @staticmethod
    def get_authors_info(obj):
        if not obj.authors:
            book = Book.objects.get(id=obj.id)
            authors = book.authors.all()
        else:
            authors = obj.authors.all()
        return [{'id': author.id, 'name': author.name, 'avatar': author.avatar} for author in authors]

    @staticmethod
    def get_publisher_info(obj):
        if not obj.publisher:
            book = Book.objects.all().get(id=obj.id)
            publisher = book.publisher
        else:
            publisher = obj.publisher
        return {'id': publisher.id, 'name': publisher.name, }

    @staticmethod
    def get_available_number(obj):
        if not obj.copies:
            book = Book.objects.get(id=obj.id)
            copies = book.copies
        else:
            copies = obj.copies
        return len(copies.filter(status='Available').all())

    @staticmethod
    def get_comment_summary(obj):
        if not obj.comment_summary:
            book = Book.objects.get(id=obj.id)
            comment_summary = book.comment_summary
        else:
            comment_summary = obj.comment_summary
        from comment.serializers import CommentSummarySerializer

        serializer = CommentSummarySerializer(comment_summary.all(), many=True)
        return serializer.data[0] if len(serializer.data) > 0 else {}

    def create(self, validated_data):
        copies = validated_data.pop('copies')
        book = super(BookSerializer, self).create(validated_data)
        self.save_copies(copies, book)
        return book

    def update(self, instance, validated_data):
        copies = validated_data.pop('copies')
        book = super(BookSerializer, self).update(instance, validated_data)
        self.save_copies(copies, book)
        return book

    @staticmethod
    def save_copies(copies, book: Book):
        new_copies_data = []
        update_copies_data = []
        barcode_list = gen_barcode(len(copies))
        fields = []
        for index, copy in enumerate(copies):
            if not copy.get('id'):
                new_copy = {
                    'barcode': barcode_list[index],
                    'creator': book.creator,
                    'modifier': book.modifier,
                    'status': Constant.BOOK_STATUS_AVAILABLE,
                    **copy,
                }
                if 'book' not in copy:
                    new_copy['book'] = book
                new_copies_data.append(BookCopy(**new_copy))
            else:
                update_copy = {
                    'modifier': book.modifier,
                    **copy,
                }
                if not update_copies_data:
                    fields = list(update_copy.keys())
                    fields.remove('id')
                update_copies_data.append(BookCopy(**update_copy))
        if new_copies_data:
            BookCopy.objects.bulk_create(new_copies_data)
        if update_copies_data:
            BookCopy.objects.bulk_update(update_copies_data, fields)


def gen_barcode(num):
    """
    Generate book copy's barcode
    :param num: number of book copy
    :return: a barcode list which size is save as num
    """
    ret = []
    copy_cnt = BookCopy.objects.count()
    if not copy_cnt:
        max_barcode_int = 1000000001
    else:
        max_barcode_int = int(BookCopy.objects.aggregate(Max('barcode'))['barcode__max']) + 1
    for i in range(num):
        ret.append(str(max_barcode_int))
        max_barcode_int += 1

    return ret
