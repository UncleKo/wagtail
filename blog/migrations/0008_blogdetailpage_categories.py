# Generated by Django 3.1.7 on 2021-04-07 12:24

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
