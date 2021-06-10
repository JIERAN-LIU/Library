# Create your models here.
from django.db.models import Model, ForeignKey, DO_NOTHING, DateTimeField, BooleanField, FloatField, CharField

from book.models import Book, BookCopy
from common.constant import Constant
from common.models import AbstractLibraryBaseModel, User


class BorrowRecord(AbstractLibraryBaseModel):
    book = ForeignKey(Book, verbose_name='Book', on_delete=DO_NOTHING, null=True, blank=True,
                      related_name='borrowed_book')
    copy = ForeignKey(BookCopy, verbose_name='Copy', on_delete=DO_NOTHING, null=True, blank=True,
                      related_name='borrowed_copy')
    reader = ForeignKey(User, verbose_name='Borrowed by', on_delete=DO_NOTHING, null=True, blank=True,
                        related_name='borrow_record_reader')
    borrowed_at = DateTimeField(verbose_name='borrowed_at', auto_now_add=True)
    returned_at = DateTimeField(verbose_name='returned_at', null=True, blank=True)
    renewed_at = DateTimeField(verbose_name='renewed_at', null=True, blank=True)
    fined_at = DateTimeField(verbose_name='fined_at', null=True, blank=True)
    has_returned = BooleanField('Returned', default=False)
    has_renewed = BooleanField('Renewed', default=False)
    has_overdue = BooleanField('Overdue', default=False)
    has_fined = BooleanField('Fined', default=False)
    fine = FloatField('Fine', default=None, null=True)
    pay_method = CharField('Method', max_length=100, choices=Constant.PAY_METHODS, null=True)
    currency_symbol = CharField('Symbol', max_length=100, choices=Constant.CURRENCY_SYMBOLS,
                                null=True)

    class Meta:
        db_table = 'library_borrow_record'
