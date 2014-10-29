# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import mptt.fields

template_choices = [(x, y) for x, y in settings.RESOURCES_TEMPLATES]


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
            bases=(models.Model,),
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='resources.Resource')),
                ('show_title', models.BooleanField(default=True)),
                ('meta_summary', models.TextField(blank=True)),
                ('text', models.TextField(blank=True)),
                ('template', models.CharField(default=None, help_text='Inherit if empty', max_length=100, blank=True, choices=template_choices)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Page',
            },
            bases=('resources.resource',),
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceCollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.PositiveSmallIntegerField()),
                ('collection', models.ForeignKey(to='resources.ResourceCollection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20)),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Weblink',
            fields=[
                ('resource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='resources.Resource')),
                ('target', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('resources.resource',),
        ),
        migrations.AddField(
            model_name='resourceproperty',
            name='resource',
            field=models.ForeignKey(to='resources.Resource'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resourceproperty',
            unique_together=set([('resource', 'key')]),
        ),
        migrations.AddField(
            model_name='resourcecollectionitem',
            name='resource',
            field=models.ForeignKey(to='resources.Resource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name=b'children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='resources.Resource', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='translation_pool',
            field=models.ForeignKey(editable=False, to='resources.ResourceTranslation', verbose_name='Translation pool'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('slug', 'language'), ('translation_pool', 'language')]),
        ),
    ]
