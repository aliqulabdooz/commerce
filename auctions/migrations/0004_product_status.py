# Generated by Django 5.1.3 on 2024-11-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_comment_product_comment_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('end', 'ending bid'), ('start', 'starting bid')], default='start', max_length=5),
        ),
    ]
