# Generated by Django 2.2.1 on 2019-06-06 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraped_suits', '0002_auto_20190523_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('currency', models.CharField(default='GBP', max_length=3)),
                ('suit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraped_suits.Suit')),
            ],
        ),
    ]
