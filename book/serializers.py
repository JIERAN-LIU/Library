from rest_framework import serializers

from book.models import Book, Publisher, Author, BookCopy


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'email', 'logo', 'site']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'gender', 'nation', 'avatar', 'profile', 'birthday', 'died_at']


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'barcode', 'status', 'location', 'section', 'media_type']
        extra_kwargs = {
            'barcode': {'read_only': True},
        }


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']


class BookSerializer(serializers.ModelSerializer):
    copies = BookCopySerializer(many=True)
    publisher = serializers.SerializerMethodField(read_only=True)
    authors = serializers.SerializerMethodField(read_only=True)
    available_number = serializers.SerializerMethodField(read_only=True)
    comment_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'language', 'subject', 'cover', 'description', 'isbn_10', 'isbn_13', 'publisher',
                  'publication_date', 'call_number', 'authors', 'toc', 'price', 'print_length', 'binding', 'copies',
                  'comment_summary', 'available_number']

        extra_kwargs = {
            'call_number': {'read_only': True},
        }

    @staticmethod
    def get_authors(obj):
        if not obj.authors:
            book = Book.objects.get(id=obj.id)
            authors = book.authors.all()
        else:
            authors = obj.authors.all()
        return [{'id': author.id, 'name': author.name, 'avatar': author.avatar} for author in authors]

    @staticmethod
    def get_publisher(obj):
        if not obj.publisher:
            book = Book.objects.get(id=obj.id)
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

