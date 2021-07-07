from haystack import indexes

from book.models import Book, Author, Publisher
from common.constant import Constant


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id', stored=True)
    title = indexes.EdgeNgramField(model_attr='title')
    authors_name = indexes.EdgeNgramField(model_attr='authors_name')
    publisher_name = indexes.EdgeNgramField(model_attr='publisher_name')
    publication_date = indexes.DateTimeField(model_attr='publication_date')
    description = indexes.CharField(model_attr='description')
    isbn_10 = indexes.EdgeNgramField(model_attr='isbn_10')
    isbn_13 = indexes.EdgeNgramField(model_attr='isbn_13')
    toc = indexes.CharField(model_attr='toc')
    binding = indexes.CharField(model_attr='binding')
    language = indexes.CharField(model_attr='language')
    subject = indexes.CharField(model_attr='subject')
    call_number = indexes.EdgeNgramField(model_attr='call_number')
    price = indexes.FloatField(model_attr='price', stored=True)
    print_length = indexes.IntegerField(model_attr='print_length', stored=True)
    cover = indexes.CharField(model_attr='cover', stored=True)

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.filter().exclude(status=Constant.BOOK_STATUS_DELETED)


class AuthorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id', stored=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Author

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PublisherIndex(AuthorIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id', stored=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Publisher
