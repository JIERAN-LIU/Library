# Generated by Django 2.2.23 on 2021-06-21 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.IntegerField(null=True, verbose_name='creator')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modifier', models.IntegerField(null=True, verbose_name='modifier')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('borrowed_at', models.DateTimeField(auto_now_add=True, verbose_name='borrowed_at')),
                ('returned_at', models.DateTimeField(blank=True, null=True, verbose_name='returned_at')),
                ('renewed_at', models.DateTimeField(blank=True, null=True, verbose_name='renewed_at')),
                ('fined_at', models.DateTimeField(blank=True, null=True, verbose_name='fined_at')),
                ('has_returned', models.BooleanField(default=False, verbose_name='Returned')),
                ('has_renewed', models.BooleanField(default=False, verbose_name='Renewed')),
                ('has_overdue', models.BooleanField(default=False, verbose_name='Overdue')),
                ('has_fined', models.BooleanField(default=False, verbose_name='Fined')),
                ('fine', models.FloatField(default=None, null=True, verbose_name='Fine')),
                ('pay_method', models.CharField(choices=[('Cash', 'Cash'), ('Paypal', 'Paypal'), ('Credit card', 'Credit card')], max_length=100, null=True, verbose_name='Method')),
                ('currency_symbol', models.CharField(choices=[('THB', '฿'), ('USD', '$'), ('CNY', '￥'), ('GBP', '￡'), ('DEM', 'DM.'), ('FRP', 'FF'), ('ESP', 'Pts.'), ('JPY', 'J.')], max_length=100, null=True, verbose_name='Symbol')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrowed_book', to='book.Book', verbose_name='Book')),
                ('copy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrowed_copy', to='book.BookCopy', verbose_name='Copy')),
            ],
            options={
                'db_table': 'library_borrow_record',
            },
        ),
    ]
