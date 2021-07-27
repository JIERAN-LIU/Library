# Create your models here.

from django.db.models import Model, CharField, EmailField, URLField, IntegerField, TextField, \
    ForeignKey, DO_NOTHING, FloatField, ManyToManyField, CASCADE, DateField

from common.constant import Constant
from common.models import AbstractLibraryBaseModel


class Publisher(AbstractLibraryBaseModel):
    name = CharField('Name', max_length=100, unique=True)
    email = EmailField('Email')
    logo = CharField('Logo', max_length=1000)
    site = URLField('Site')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'library_publisher'


class Author(AbstractLibraryBaseModel):
    name = CharField('Name', max_length=100)
    nation = CharField('Nation', max_length=100, choices=Constant.NATIONALITY)
    avatar = CharField('Avatar', max_length=1000)
    gender = CharField('gender', max_length=1000, choices=Constant.GENDERS, default='Male')
    profile = TextField('Profile', max_length=10000)
    birthday = DateField(default=None, verbose_name='Birthday')
    died_at = DateField(default=None, verbose_name='Died at', null=True)

    def __str__(self):
        return '{}[{}]'.format(self.name, self.nation)

    class Meta:
        db_table = 'library_author'


class Book(AbstractLibraryBaseModel):
    title = CharField('Title', max_length=100)
    language = CharField('Language', max_length=100, choices=Constant.LANGUAGES)
    subject = CharField('Subject', max_length=100, choices=Constant.BOOK_SUBJECTS)
    cover = CharField('Cover', max_length=1000)
    description = TextField('Description', max_length=10000)
    isbn_10 = CharField('ISBN-10', max_length=100)
    isbn_13 = CharField('ISBN-13', max_length=100)
    call_number = CharField('Call number', max_length=100, unique=True)
    publisher = ForeignKey(Publisher, verbose_name='Published By', on_delete=DO_NOTHING, null=True,
                           related_name='book_publisher')
    publication_date = DateField(default=None, verbose_name='Publication Date')
    authors = ManyToManyField(Author, verbose_name='Author', related_name='book_author')
    toc = TextField('ToC', max_length=10000)
    price = FloatField('Price')
    print_length = IntegerField('Print length', default=1)
    binding = CharField('Binding', max_length=100, choices=Constant.BINDINGS)
    status = CharField('Status', max_length=100, choices=Constant.BOOK_STATUS, default=Constant.BOOK_STATUS_AVAILABLE)

    def __str__(self):
        return '{}[{}]'.format(self.title, self.language)

    @property
    def publisher_name(self):
        publisher = self.publisher
        if not publisher:
            return ""
        return publisher.name

    @property
    def authors_name(self):
        authors = self.authors
        if not authors:
            return ""
        return ", ".join([author.name for author in authors.all()])

    class Meta:
        db_table = 'library_book'


class BookCopy(AbstractLibraryBaseModel):
    book = ForeignKey(Book, verbose_name='Book', on_delete=CASCADE, related_name='copies',
                      null=False)
    barcode = CharField('Barcode', max_length=100, unique=True)
    status = CharField('Status', max_length=100, choices=Constant.BOOK_COPY_STATUS)
    location = CharField('Location', max_length=100)
    section = CharField('Section', max_length=100)
    media_type = CharField('Media type', max_length=100, choices=Constant.BOOK_MEDIA_TYPE)

    def __str__(self):
        return '{}.[{}]'.format(self.book.title, self.barcode)

    class Meta:
        db_table = 'library_book_copy'
