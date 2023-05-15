# Generated by Django 4.2.1 on 2023-05-11 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_remove_category_banner_remove_category_banner2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='extra_blocks',
            field=models.CharField(choices=[('JOB_POST', 'JOB_POST'), ('SALARY_RANGE_BLOCK', 'SALARY_RANGE_BLOCK')], default='JOB_POST', max_length=20),
        ),
        migrations.AlterField(
            model_name='blog',
            name='job_area',
            field=models.CharField(choices=[('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('EU_COUNTRIES', 'EU_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
    ]
