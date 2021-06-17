from drf_haystack.serializers import HaystackSerializer

from book.serializers import BookSerializer, AuthorSerializer, PublisherSerializer
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
