# Generated by Django 4.2.1 on 2023-05-09 09:20

import core.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Page Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('is_active', models.BooleanField(default=True)),
                ('add_to_page_menu', models.BooleanField(default=False)),
                ('add_to_header_menu', models.BooleanField(default=False)),
                ('add_to_footer_menu', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(default='<i class="fa-solid fa-calendar-check"></i>', help_text='HTML Fontawesoome icon', max_length=250, verbose_name='FA Icon')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='category/banner', verbose_name='Banner')),
                ('add_to_cat_menu', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(default=2, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.category', verbose_name='Parent')),
                ('sites', models.ManyToManyField(related_name='%(app_label)s_%(class)s_sites', to='sites.site')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model, core.mixins.SaveFromAdminMixin),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Page Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('is_active', models.BooleanField(default=True)),
                ('add_to_page_menu', models.BooleanField(default=False)),
                ('add_to_header_menu', models.BooleanField(default=False)),
                ('add_to_footer_menu', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(verbose_name='Body')),
                ('categories', models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_category', to='core.category', verbose_name='Categories')),
                ('creator', models.ForeignKey(default=2, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.page', verbose_name='Parent')),
                ('sites', models.ManyToManyField(related_name='%(app_label)s_%(class)s_sites', to='sites.site')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model, core.mixins.SaveFromAdminMixin),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Page Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('add_to_page_menu', models.BooleanField(default=False)),
                ('add_to_header_menu', models.BooleanField(default=False)),
                ('add_to_footer_menu', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.ImageField(upload_to='blog/feature_image/', verbose_name='Feature Image')),
                ('body', models.TextField(verbose_name='Body')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('unpublished', 'UnPublished')], max_length=20)),
                ('categories', models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_category', to='core.category', verbose_name='Categories')),
                ('creator', models.ForeignKey(default=2, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.blog', verbose_name='Parent')),
                ('sites', models.ManyToManyField(related_name='%(app_label)s_%(class)s_sites', to='sites.site')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
            bases=(models.Model, core.mixins.SaveFromAdminMixin),
        ),
    ]
