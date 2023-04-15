# Generated by Django 3.1.7 on 2021-12-15 13:20

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=5, verbose_name='Позиция')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна')),
            ],
            options={
                'verbose_name': 'Вопросс FAQ',
                'verbose_name_plural': 'Вопросы FAQ',
                'ordering': ('order',),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TextPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='SLUG')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна')),
                ('ordering', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Текстовая страница',
                'verbose_name_plural': 'Текстовые страницы',
                'ordering': ('ordering',),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TextPageTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Контент')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='text_pages.textpage')),
            ],
            options={
                'verbose_name': 'Текстовая страница Translation',
                'db_table': 'text_pages_textpage_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FAQQuestionTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('question', models.CharField(max_length=150, verbose_name='Вопрос')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Ответ')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='text_pages.faqquestion')),
            ],
            options={
                'verbose_name': 'Вопросс FAQ Translation',
                'db_table': 'text_pages_faqquestion_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
