# Generated by Django 4.2.1 on 2023-05-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_action_action_type_alter_blog_extra_blocks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='job_area',
            field=models.CharField(choices=[('ASIAN_COUNTRIES', 'ASIAN_COUNTRIES'), ('AMERICAN_COUNTRIES', 'AMERICAN_COUNTRIES'), ('OCENIA_COUNTRIES', 'OCENIA_COUNTRIES'), ('AFRICAN_COUNTRIES', 'AFRICAN_COUNTRIES'), ('MIDDLEEAST_COUNTRIES', 'MIDDLEEAST_COUNTRIES'), ('EU_COUNTRIES', 'EU_COUNTRIES')], default='EU_COUNTRIES', max_length=20),
        ),
    ]