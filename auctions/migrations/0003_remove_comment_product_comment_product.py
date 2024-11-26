# Generated by Django 5.1.3 on 2024-11-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_comments_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='product',
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ManyToManyField(related_name='product_comment', to='auctions.product'),
        ),
    ]
