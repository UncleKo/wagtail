# Generated by Django 3.1.7 on 2021-04-16 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_blogpagination'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogParentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'verbose_name': '親カテゴリー',
                'verbose_name_plural': '親カテゴリー',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='blog.blogparentcategory', verbose_name='親カテゴリー'),
        ),
    ]