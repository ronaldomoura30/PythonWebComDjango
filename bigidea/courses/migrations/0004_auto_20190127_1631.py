# Generated by Django 2.1.5 on 2019-01-27 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190127_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(max_length=60, unique=True, verbose_name='Atalho'),
        ),
    ]