# Generated by Django 3.1.7 on 2021-12-15 13:20

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import utils.models.banners


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner404',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Название баннера')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('desktop_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для десктопа')),
                ('mobile_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для мобильных')),
                ('button_left_link', models.URLField(verbose_name='Ссылка левой кнопки')),
                ('button_right_link', models.URLField(verbose_name='Ссылка правой кнопки')),
                ('button_left_color', models.CharField(default='#000000', max_length=15, verbose_name='Цвет левой кнопки (HEX)')),
                ('button_right_color', models.URLField(default='#000000', max_length=15, verbose_name='Цвет правой кнопки (HEX)')),
                ('button_left_text_color', models.CharField(default='#ffffff', max_length=15, verbose_name='Цвет текста левой кнопки (HEX)')),
                ('button_right_text_color', models.URLField(default='#ffffff', max_length=15, verbose_name='Цвет текста правой кнопки (HEX)')),
            ],
            options={
                'verbose_name': '404 страница',
                'verbose_name_plural': '404 страница',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=1023, verbose_name='Слаг')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('location', models.CharField(choices=[('main_page', 'На главной'), ('page_404', 'Страница 404')], default='main_page', max_length=255, verbose_name='Расположение')),
                ('category', models.ManyToManyField(blank=True, related_name='category_blocks', to='catalog.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Блок с категориями',
                'verbose_name_plural': 'Блок с категориями',
                'ordering': ('order',),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ru_name', models.CharField(max_length=100, verbose_name='Название города RU')),
                ('en_name', models.CharField(max_length=100, verbose_name='Название города EN')),
                ('country', models.CharField(max_length=100, null=True, verbose_name='Страна')),
                ('iso', models.CharField(max_length=10, null=True, verbose_name='ISO страны')),
                ('zip_code', models.CharField(max_length=30, null=True, verbose_name='Индекс')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'База городов',
            },
        ),
        migrations.CreateModel(
            name='MainBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Название баннера')),
                ('link', models.CharField(blank=True, max_length=2000, verbose_name='Ссылка с баннера')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Позиция')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('desktop_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для десктопа')),
                ('mobile_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для мобильных')),
            ],
            options={
                'verbose_name': 'Главный баннер',
                'verbose_name_plural': 'Главный баннер',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SecondBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Название баннера')),
                ('link', models.CharField(blank=True, max_length=2000, verbose_name='Ссылка с баннера')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Позиция')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('desktop_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для десктопа')),
                ('mobile_image', models.FileField(blank=True, upload_to=utils.models.banners.get_upload_path, verbose_name='Изображение для мобильных')),
            ],
            options={
                'verbose_name': 'Второй баннер',
                'verbose_name_plural': 'Вторые баннеры',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yandex_market_link', models.CharField(blank=True, max_length=500, verbose_name='Ссылка на Yandex Market')),
                ('vk_link', models.CharField(blank=True, max_length=500, verbose_name='Ссылка на VK')),
                ('instagram_link', models.CharField(blank=True, max_length=500, verbose_name='Ссылка на Instagram')),
                ('site_phone', models.CharField(blank=True, max_length=500, verbose_name='Телефон на сайте')),
                ('site_email', models.CharField(blank=True, max_length=500, verbose_name='Email на сайте')),
                ('ceo_email_for_contacts', models.CharField(blank=True, max_length=500, verbose_name='Email для обращений к руководителю')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TempFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='tmp/')),
            ],
        ),
        migrations.CreateModel(
            name='SiteSettingsTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('header_offer', models.CharField(blank=True, max_length=500, verbose_name='Предложение в шапке сайта')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='utils.sitesettings')),
            ],
            options={
                'verbose_name': 'Настройки сайта Translation',
                'db_table': 'utils_sitesettings_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SecondBannerTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок баннера')),
                ('subtitle', models.CharField(blank=True, max_length=500, verbose_name='Подзаголовок баннера')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='utils.secondbanner')),
            ],
            options={
                'verbose_name': 'Второй баннер Translation',
                'db_table': 'utils_secondbanner_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MainBannerTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок баннера')),
                ('button_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст кнопки баннера')),
                ('subtitle', models.CharField(blank=True, max_length=500, verbose_name='Подзаголовок баннера')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='utils.mainbanner')),
            ],
            options={
                'verbose_name': 'Главный баннер Translation',
                'db_table': 'utils_mainbanner_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryBlockTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=1023, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=1023, verbose_name='Описание')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='utils.categoryblock')),
            ],
            options={
                'verbose_name': 'Блок с категориями Translation',
                'db_table': 'utils_categoryblock_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Banner404Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок баннера')),
                ('subtitle', models.CharField(blank=True, max_length=500, verbose_name='Подзаголовок баннера')),
                ('button_left_text', models.CharField(blank=True, max_length=500, verbose_name='Текст левой кнопки')),
                ('button_right_text', models.CharField(blank=True, max_length=500, verbose_name='Текст правой кнопки')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='utils.banner404')),
            ],
            options={
                'verbose_name': '404 страница Translation',
                'db_table': 'utils_banner404_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
