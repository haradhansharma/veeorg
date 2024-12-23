# Generated by Django 4.2.1 on 2023-05-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_remove_action_total_likes_remove_action_total_views_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('unpublished', 'UnPublished')], default='published', max_length=20),
        ),
        migrations.AlterField(
            model_name='blog',
            name='extra_blocks',
            field=models.CharField(choices=[('SALARY_RANGE_BLOCK', 'SALARY_RANGE_BLOCK'), ('JOB_POST', 'JOB_POST')], default='JOB_POST', max_length=20),
        ),
        migrations.AlterField(
            model_name='blog',
            name='job_area',
            field=models.CharField(choices=[('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('EU_COUNTRIES', 'EU_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
    ]
