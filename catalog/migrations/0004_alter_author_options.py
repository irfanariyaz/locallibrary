# Generated by Django 4.0.2 on 2022-02-24 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_book_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]