# Generated by Django 3.1.7 on 2021-04-12 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0007_homepagecarouselimages_image_alt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagecarouselimages',
            name='carousel_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
