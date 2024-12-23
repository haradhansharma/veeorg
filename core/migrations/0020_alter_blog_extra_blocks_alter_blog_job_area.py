# Generated by Django 4.2.1 on 2023-05-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_rename_cat_description_category_description_and_more'),
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
            field=models.CharField(choices=[('EU_COUNTRIES', 'EU_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
    ]
