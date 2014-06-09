# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Checkout'
        db.create_table('pagseguro_checkout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('success', self.gf('django.db.models.fields.BooleanField')(db_index=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pagseguro', ['Checkout'])

        # Adding model 'Transaction'
        db.create_table('pagseguro_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_event_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('pagseguro', ['Transaction'])

        # Adding model 'TransactionHistory'
        db.create_table('pagseguro_transactionhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagseguro.Transaction'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('pagseguro', ['TransactionHistory'])


    def backwards(self, orm):
        # Deleting model 'Checkout'
        db.delete_table('pagseguro_checkout')

        # Deleting model 'Transaction'
        db.delete_table('pagseguro_transaction')

        # Deleting model 'TransactionHistory'
        db.delete_table('pagseguro_transactionhistory')


    models = {
        'pagseguro.checkout': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Checkout'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'db_index': 'True'})
        },
        'pagseguro.transaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Transaction'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_event_date': ('django.db.models.fields.DateTimeField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'})
        },
        'pagseguro.transactionhistory': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TransactionHistory'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagseguro.Transaction']"})
        }
    }

    complete_apps = ['pagseguro']