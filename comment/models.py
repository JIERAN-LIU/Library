# Create your models here.
from django.db.models import CASCADE, ForeignKey, TextField, IntegerField, Model, FloatField, OneToOneField, DO_NOTHING

from book.models import Book
from common.models import AbstractLibraryBaseModel, User


class Comment(AbstractLibraryBaseModel):
    user = ForeignKey(User, verbose_name='User', on_delete=DO_NOTHING, related_name='comment_user', null=True)
    book = ForeignKey(Book, verbose_name='Book', on_delete=DO_NOTHING, related_name='comment_book', null=True)
    content = TextField('Content', max_length=10000, null=True)
    rating = IntegerField('Rating', choices=[(i, i) for i in range(11)], null=False)

    class Meta:
        db_table = 'library_comment'

    def __str__(self):
        return str(self.rating)


class CommentSummary(Model):
    book = ForeignKey(Book, verbose_name='Book', on_delete=CASCADE, related_name='comment_summary', null=False)
    rating = FloatField('Rating')
    rating_number = IntegerField('Rating number')

    class Meta:
        db_table = 'library_comment_summary'

    def __str__(self):
        return 'mean rating {} from {}'.format(self.rating, self.rating_number)