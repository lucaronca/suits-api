# Generated by Django 2.2.1 on 2019-05-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=150)),
                ('color', models.CharField(max_length=150)),
                ('fit', models.CharField(max_length=150)),
                ('material', models.CharField(max_length=150)),
                ('image', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Suit scraped from website',
            },
        ),
    ]