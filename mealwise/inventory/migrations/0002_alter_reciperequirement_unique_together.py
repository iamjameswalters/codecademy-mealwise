# Generated by Django 3.2.9 on 2021-12-03 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reciperequirement',
            unique_together={('menu_item', 'ingredient')},
        ),
    ]
