# Generated by Django 3.1.7 on 2021-04-07 07:21

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogauthorsorderable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthorsorderable',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_authors', to='blog.blogdetailpage'),
        ),
    ]
