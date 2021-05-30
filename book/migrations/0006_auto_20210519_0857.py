# Generated by Django 2.2.5 on 2021-05-19 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20210518_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='binding',
            field=models.CharField(choices=[('Paperback', 'Paperback'), ('Hardback', 'Hardback'), ('Thread', 'Thread')], max_length=100, verbose_name='Binding'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('th-TH', 'Thai'), ('en-US', 'English'), ('zh-CN', 'Chinese(Simplified)'), ('zh-TW', 'Chinese(Traditional)'), ('es-ES', 'Spanish'), ('de-DE', 'German'), ('fr-FR', 'French'), ('ja-JP', 'Japanese')], max_length=100, verbose_name='Language'),
        ),
    ]
