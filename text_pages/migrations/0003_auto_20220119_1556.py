# Generated by Django 3.1.7 on 2022-01-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_pages', '0002_auto_20220119_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpage',
            name='show_in_footer',
            field=models.BooleanField(default=False, verbose_name='Отображать в футере'),
        ),
        migrations.AlterField(
            model_name='textpagetranslation',
            name='seo_content',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='SEO Контент'),
        ),
        migrations.AlterField(
            model_name='textpagetranslation',
            name='seo_title',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='SEO Заголовок'),
        ),
    ]
