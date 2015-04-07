# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import ckeditor.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.FileField(upload_to=b'file')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.SlugField(editable=False)),
                ('title', models.CharField(max_length=100)),
                ('menu_title', models.CharField(max_length=100, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('in_menu', models.BooleanField(default=True, db_index=True)),
                ('noindex', models.BooleanField(default=False, verbose_name=b'Do not index')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True, db_index=True)),
                ('published', models.DateTimeField(null=True, blank=True)),
                ('unpublished', models.DateTimeField(null=True, blank=True)),
                ('language', models.CharField(default=b'en', max_length=5, db_index=True, choices=[(b'en', b'English'), (b'de', b'Deutsch')])),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
        migrations.CreateModel(
            name='ResourceCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Resource collection',
                'verbose_name_plural': 'Resource collections',
            },
        ),
        migrations.CreateModel(
            name='ResourceCollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.PositiveSmallIntegerField()),
                ('collection', models.ForeignKey(to='HavelCMS.ResourceCollection')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ResourceTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Resource translation',
                'verbose_name_plural': 'Resource translations',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='HavelCMS.Resource')),
                ('show_title', models.BooleanField(default=True)),
                ('meta_summary', models.TextField(blank=True)),
                ('text', ckeditor.fields.RichTextField(blank=True)),
                ('template', models.CharField(default=None, help_text='Inherit if empty', max_length=100, blank=True, choices=[(b'default.html', b'Default CMS template')])),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Page',
            },
            bases=('HavelCMS.resource',),
        ),
        migrations.CreateModel(
            name='Weblink',
            fields=[
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='HavelCMS.Resource')),
                ('target', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('HavelCMS.resource',),
        ),
        migrations.AddField(
            model_name='resourceproperty',
            name='resource',
            field=models.ForeignKey(to='HavelCMS.Resource'),
        ),
        migrations.AddField(
            model_name='resourcecollectionitem',
            name='resource',
            field=models.ForeignKey(to='HavelCMS.Resource'),
        ),
        migrations.AddField(
            model_name='resource',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='HavelCMS.Resource', null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='translation_pool',
            field=models.ForeignKey(editable=False, to='HavelCMS.ResourceTranslation', verbose_name='Translation pool'),
        ),
        migrations.AlterUniqueTogether(
            name='resourceproperty',
            unique_together=set([('resource', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('slug', 'language'), ('translation_pool', 'language')]),
        ),
    ]
