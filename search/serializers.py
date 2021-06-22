from drf_haystack.serializers import HaystackSerializer

from book.serializers import BookSerializer, AuthorSerializer, PublisherSerializer
from search.search_indexes import BookIndex, AuthorIndex, PublisherIndex
from search.utils import HighlightedCharField


class BookIndexSerializer(HaystackSerializer, BookSerializer):
    title = HighlightedCharField()
    description = HighlightedCharField()
    toc = HighlightedCharField()
    publisher_name = HighlightedCharField()
    language = HighlightedCharField()
    binding = HighlightedCharField()
    call_number = HighlightedCharField()
    isbn_10 = HighlightedCharField()
    isbn_13 = HighlightedCharField()
    subject = HighlightedCharField()

    class Meta(BookSerializer.Meta):
        index_classes = [BookIndex]
        search_fields = ['text', ]


class BookAutocompleteSerializer(HaystackSerializer, BookSerializer):
    class Meta(BookSerializer.Meta):
        index_classes = [BookIndex]
        fields = ['id', 'title', 'publisher_name', 'subject', 'authors_name', 'language']
        ignore_fields = ["autocomplete"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "title"
        }


class AuthorIndexSerializer(HaystackSerializer, AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = ['id', 'name']
        index_classes = [AuthorIndex]
        search_fields = ['text', ]


class PublisherIndexSerializer(HaystackSerializer, PublisherSerializer):
    class Meta(PublisherSerializer.Meta):
        fields = ['id', 'name']
        index_classes = [PublisherIndex]
        search_fields = ['text', ]
