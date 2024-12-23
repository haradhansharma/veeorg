# Generated by Django 4.2.1 on 2023-05-10 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_blog_ref_link_alter_blog_job_area'),
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
            field=models.CharField(choices=[('EU_COUNTRIES', 'EU_COUNTRIES'), ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
        migrations.AlterField(
            model_name='blog',
            name='ref_link',
            field=models.URLField(default='#'),
        ),
    ]
