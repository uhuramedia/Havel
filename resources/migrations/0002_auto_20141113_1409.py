# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
