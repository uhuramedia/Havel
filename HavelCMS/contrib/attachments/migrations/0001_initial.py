# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('object_id', models.PositiveIntegerField(db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileLink',
            fields=[
                ('relatedlink_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='attachments.RelatedLink')),
                ('file', models.FileField(help_text=b'Audio MP3 or PDF, MS word files.', upload_to=b'files')),
            ],
            options={
            },
            bases=('attachments.relatedlink',),
        ),
        migrations.CreateModel(
            name='WebLink',
            fields=[
                ('relatedlink_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='attachments.RelatedLink')),
                ('link_type', models.CharField(default=b'Web', max_length=10, choices=[(b'Web', b'Web Page'), (b'Event', b'Event Link')])),
                ('url', models.URLField(max_length=400)),
            ],
            options={
            },
            bases=('attachments.relatedlink',),
        ),
        migrations.AddField(
            model_name='relatedlink',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
