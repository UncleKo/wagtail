# Generated by Django 3.1.7 on 2021-04-07 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_homepagecarouselimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagecarouselimages',
            name='image_alt',
            field=models.CharField(blank=True, help_text='Add some alt text', max_length=100, null=True),
        ),
    ]
