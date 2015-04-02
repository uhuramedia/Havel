# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ResourceProperty.value'
        db.alter_column('resources_resourceproperty', 'value', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'ResourceProperty.value'
        db.alter_column('resources_resourceproperty', 'value', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'resources.file': {
            'Meta': {'object_name': 'File'},
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'resources.page': {
            'Meta': {'object_name': 'Page', '_ormbases': ['resources.Resource']},
            'meta_summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['resources.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'one_column.html'", 'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'resources.resource': {
            'Meta': {'unique_together': "(('translation_pool', 'language'), ('slug', 'language'))", 'object_name': 'Resource'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'de'", 'max_length': '5', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'menu_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'noindex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['resources.Resource']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'translation_pool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resources.ResourceTranslation']"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'unpublished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'resources.resourcecollection': {
            'Meta': {'object_name': 'ResourceCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'resources.resourcecollectionitem': {
            'Meta': {'object_name': 'ResourceCollectionItem'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resources.ResourceCollection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resources.Resource']"}),
            'sort': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'resources.resourceproperty': {
            'Meta': {'unique_together': "(('resource', 'key'),)", 'object_name': 'ResourceProperty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resources.Resource']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'resources.resourcetranslation': {
            'Meta': {'object_name': 'ResourceTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'resources.weblink': {
            'Meta': {'object_name': 'Weblink', '_ormbases': ['resources.Resource']},
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['resources.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['resources']