# Generated by Django 3.1.7 on 2022-02-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_registrationforfitting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationforfitting',
            options={'ordering': ('time',), 'verbose_name': 'Запись на примерку', 'verbose_name_plural': 'Записи на примерку'},
        ),
        migrations.AlterField(
            model_name='registrationforfitting',
            name='service_type',
            field=models.IntegerField(choices=[(8765543, 'Примерка коротких платьев'), (8765556, 'Повторная примерка коротких платьев'), (8765563, 'Примерка длинных платьев'), (8765582, 'Повторная примерка длинных платьев'), (8765595, 'Примерка сшитого платья на заказ'), (8765051, 'Записаться на примерку')], verbose_name='Тип примерки'),
        ),
    ]
