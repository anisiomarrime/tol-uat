# Generated by Django 2.2.7 on 2020-03-06 11:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='post',
            name='exp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(default='Ola! estou no So Boladas...'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=50)),
                ('comment', models.TextField(default='Ola! quero fazer o upgrade.')),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('package', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Package')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Seller')),
            ],
        ),
    ]
