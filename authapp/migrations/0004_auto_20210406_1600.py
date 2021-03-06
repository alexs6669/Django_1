# Generated by Django 3.1.7 on 2021-04-06 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210404_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='актуальность ключа'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='возраст'),
        ),
    ]
