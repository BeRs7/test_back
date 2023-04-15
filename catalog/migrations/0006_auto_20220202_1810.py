# Generated by Django 3.1.7 on 2022-02-02 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_major_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cover_description',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Описание на обложке'),
        ),
        migrations.AddField(
            model_name='category',
            name='cover_title',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Заголовок на обложке'),
        ),
    ]