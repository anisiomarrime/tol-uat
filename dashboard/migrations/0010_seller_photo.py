# Generated by Django 2.2.7 on 2020-04-28 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_updaterequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='photo',
            field=models.CharField(default='admin.jpg', max_length=250),
        ),
    ]