# Generated by Django 4.2.1 on 2023-05-14 05:55

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_alter_blog_extra_blocks_alter_blog_job_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='extra_blocks',
            field=models.CharField(choices=[('SALARY_RANGE_BLOCK', 'SALARY_RANGE_BLOCK'), ('JOB_POST', 'JOB_POST')], default='JOB_POST', max_length=20),
        ),
        migrations.AlterField(
            model_name='blog',
            name='job_area',
            field=models.CharField(choices=[('EU_COUNTRIES', 'EU_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
        migrations.AlterField(
            model_name='cvlibrary',
            name='cv_file',
            field=models.FileField(upload_to='cv_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'], message='Only PDF allowed'), core.models.validate_file_size], verbose_name='Upload your CV PDF only'),
        ),
    ]
