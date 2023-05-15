# Generated by Django 4.2.1 on 2023-05-12 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_blog_should_as_it_is_blog_should_have_apf_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_at'], 'verbose_name': 'Blog', 'verbose_name_plural': 'Blogs'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_at'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['-created_at'], 'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='job_area',
            field=models.CharField(choices=[('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('EU_COUNTRIES', 'EU_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
    ]
