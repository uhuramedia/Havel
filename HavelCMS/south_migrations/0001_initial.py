# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table('resources_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, on_delete=models.SET_NULL, to=orm['resources.Resource'])),
            ('content_type', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('menu_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('in_menu', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('noindex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('unpublished', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('translation_pool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resources.ResourceTranslation'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='de', max_length=5, db_index=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('resources', ['Resource'])

        # Adding unique constraint on 'Resource', fields ['translation_pool', 'language']
        db.create_unique('resources_resource', ['translation_pool_id', 'language'])

        # Adding unique constraint on 'Resource', fields ['slug', 'language']
        db.create_unique('resources_resource', ['slug', 'language'])

        # Adding model 'ResourceTranslation'
        db.create_table('resources_resourcetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('resources', ['ResourceTranslation'])

        # Adding model 'ResourceProperty'
        db.create_table('resources_resourceproperty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resources.Resource'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('resources', ['ResourceProperty'])

        # Adding unique constraint on 'ResourceProperty', fields ['resource', 'key']
        db.create_unique('resources_resourceproperty', ['resource_id', 'key'])

        # Adding model 'ResourceCollection'
        db.create_table('resources_resourcecollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('resources', ['ResourceCollection'])

        # Adding model 'ResourceCollectionItem'
        db.create_table('resources_resourcecollectionitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resources.ResourceCollection'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resources.Resource'])),
            ('sort', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('resources', ['ResourceCollectionItem'])

        # Adding model 'Weblink'
        db.create_table('resources_weblink', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['resources.Resource'], unique=True, primary_key=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('resources', ['Weblink'])

        # Adding model 'Page'
        db.create_table('resources_page', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['resources.Resource'], unique=True, primary_key=True)),
            ('show_title', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meta_summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='one_column.html', max_length=100, blank=True)),
        ))
        db.send_create_signal('resources', ['Page'])

        # Adding model 'File'
        db.create_table('resources_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('resources', ['File'])


    def backwards(self, orm):
        # Removing unique constraint on 'ResourceProperty', fields ['resource', 'key']
        db.delete_unique('resources_resourceproperty', ['resource_id', 'key'])

        # Removing unique constraint on 'Resource', fields ['slug', 'language']
        db.delete_unique('resources_resource', ['slug', 'language'])

        # Removing unique constraint on 'Resource', fields ['translation_pool', 'language']
        db.delete_unique('resources_resource', ['translation_pool_id', 'language'])

        # Deleting model 'Resource'
        db.delete_table('resources_resource')

        # Deleting model 'ResourceTranslation'
        db.delete_table('resources_resourcetranslation')

        # Deleting model 'ResourceProperty'
        db.delete_table('resources_resourceproperty')

        # Deleting model 'ResourceCollection'
        db.delete_table('resources_resourcecollection')

        # Deleting model 'ResourceCollectionItem'
        db.delete_table('resources_resourcecollectionitem')

        # Deleting model 'Weblink'
        db.delete_table('resources_weblink')

        # Deleting model 'Page'
        db.delete_table('resources_page')

        # Deleting model 'File'
        db.delete_table('resources_file')


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
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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