# Generated by Django 3.1.7 on 2021-04-08 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogdetailpage_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogdetailpage',
            old_name='blog_image',
            new_name='banner_image',
        ),
    ]
