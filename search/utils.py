from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter
from rest_framework.fields import CharField


class Highlighter(HaystackHighlighter):
    """
    customer keyword highlighter to prevent haystack truncate the short text
    """

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)


class HighlightedCharField(CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        request = self.context["request"]
        query = request.query_params.get("text", None)
        if not query:
            return value
        highlighter = Highlighter(query)
        return highlighter.highlight(value)
