# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'fileobject'
        db.create_table(u'filemanager_fileobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('subfolder', self.gf('django.db.models.fields.CharField')(default='/', max_length=256)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('filetype', self.gf('django.db.models.fields.CharField')(default='norender', max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'filemanager', ['fileobject'])

        # Adding model 'thumbobject'
        db.create_table(u'filemanager_thumbobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fileobject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filemanager.fileobject'])),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('filetype', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('filex', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('filey', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'filemanager', ['thumbobject'])

        # Adding unique constraint on 'thumbobject', fields ['filex', 'filey', 'fileobject']
        db.create_unique(u'filemanager_thumbobject', ['filex', 'filey', 'fileobject_id'])

        # Adding model 'zippedobject'
        db.create_table(u'filemanager_zippedobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Project'], unique=True)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'filemanager', ['zippedobject'])

        # Adding model 'htmlobject'
        db.create_table(u'filemanager_htmlobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fileobject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filemanager.fileobject'], unique=True)),
            ('body_rendered', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'filemanager', ['htmlobject'])


    def backwards(self, orm):
        # Removing unique constraint on 'thumbobject', fields ['filex', 'filey', 'fileobject']
        db.delete_unique(u'filemanager_thumbobject', ['filex', 'filey', 'fileobject_id'])

        # Deleting model 'fileobject'
        db.delete_table(u'filemanager_fileobject')

        # Deleting model 'thumbobject'
        db.delete_table(u'filemanager_thumbobject')

        # Deleting model 'zippedobject'
        db.delete_table(u'filemanager_zippedobject')

        # Deleting model 'htmlobject'
        db.delete_table(u'filemanager_htmlobject')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'filemanager.fileobject': {
            'Meta': {'object_name': 'fileobject'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'filetype': ('django.db.models.fields.CharField', [], {'default': "'norender'", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subfolder': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '256'})
        },
        u'filemanager.htmlobject': {
            'Meta': {'object_name': 'htmlobject'},
            'body_rendered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fileobject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.fileobject']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'filemanager.thumbobject': {
            'Meta': {'unique_together': "(('filex', 'filey', 'fileobject'),)", 'object_name': 'thumbobject'},
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fileobject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.fileobject']"}),
            'filetype': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'filex': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'filey': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'filemanager.zippedobject': {
            'Meta': {'object_name': 'zippedobject'},
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['project.Project']", 'unique': 'True'})
        },
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'allow_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': u"orm['auth.User']", 'related_name': "'author'", 'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bodyFile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'readme'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['filemanager.fileobject']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downloadcount_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'downloadcount_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ratingCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ratingSortBest': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'thumbnail'", 'on_delete': 'models.SET_DEFAULT', 'default': 'None', 'to': u"orm['filemanager.fileobject']", 'blank': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['filemanager']