# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Repository'
        db.create_table('dashboard_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('most_recent_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1, 1, 1, 0, 0))),
            ('from_feed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('web_url', self.gf('django.db.models.fields.URLField')(max_length=128)),
            ('clone_url', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('vcs', self.gf('django.db.models.fields.CharField')(default='git', max_length=3)),
            ('repo_rss', self.gf('django.db.models.fields.URLField')(max_length=128)),
            ('cmd', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('dashboard', ['Repository'])

        # Adding model 'Blog'
        db.create_table('dashboard_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('most_recent_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1, 1, 1, 0, 0))),
            ('from_feed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('rss', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Blog'])

        # Adding model 'Project'
        db.create_table('dashboard_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('repository', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dashboard.Repository'], unique=True)),
            ('blog', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dashboard.Blog'], unique=True)),
            ('wiki', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('presentations', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('dashboard', ['Project'])

        # Adding M2M table for field authors on 'Project'
        db.create_table('dashboard_project_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['dashboard.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('dashboard_project_authors', ['project_id', 'user_id'])

        # Adding model 'AuthorRequest'
        db.create_table('dashboard_authorrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Project'])),
            ('autodetected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dashboard', ['AuthorRequest'])

        # Adding model 'Event'
        db.create_table('dashboard_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('from_feed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Project'], null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('author_email', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Event'])

        # Adding model 'BlogPost'
        db.create_table('dashboard_blogpost', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dashboard.Event'], unique=True, primary_key=True)),
            ('markdown', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Blog'])),
            ('external_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['BlogPost'])

        # Adding model 'Commit'
        db.create_table('dashboard_commit', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dashboard.Event'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('diff', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Repository'])),
        ))
        db.send_create_signal('dashboard', ['Commit'])

        # Adding model 'Contributor'
        db.create_table('dashboard_contributor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Contributor'])

        # Adding M2M table for field projects on 'Contributor'
        db.create_table('dashboard_contributor_projects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contributor', models.ForeignKey(orm['dashboard.contributor'], null=False)),
            ('project', models.ForeignKey(orm['dashboard.project'], null=False))
        ))
        db.create_unique('dashboard_contributor_projects', ['contributor_id', 'project_id'])

        # Adding model 'Screenshot'
        db.create_table('dashboard_screenshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Project'])),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('dashboard', ['Screenshot'])

        # Adding model 'Share'
        db.create_table('dashboard_share', (
            ('event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dashboard.Event'], unique=True, primary_key=True)),
            ('external_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('link_display', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Share'])


    def backwards(self, orm):
        
        # Deleting model 'Repository'
        db.delete_table('dashboard_repository')

        # Deleting model 'Blog'
        db.delete_table('dashboard_blog')

        # Deleting model 'Project'
        db.delete_table('dashboard_project')

        # Removing M2M table for field authors on 'Project'
        db.delete_table('dashboard_project_authors')

        # Deleting model 'AuthorRequest'
        db.delete_table('dashboard_authorrequest')

        # Deleting model 'Event'
        db.delete_table('dashboard_event')

        # Deleting model 'BlogPost'
        db.delete_table('dashboard_blogpost')

        # Deleting model 'Commit'
        db.delete_table('dashboard_commit')

        # Deleting model 'Contributor'
        db.delete_table('dashboard_contributor')

        # Removing M2M table for field projects on 'Contributor'
        db.delete_table('dashboard_contributor_projects')

        # Deleting model 'Screenshot'
        db.delete_table('dashboard_screenshot')

        # Deleting model 'Share'
        db.delete_table('dashboard_share')


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
        'dashboard.authorrequest': {
            'Meta': {'object_name': 'AuthorRequest'},
            'autodetected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.blog': {
            'Meta': {'object_name': 'Blog'},
            'from_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'most_recent_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'rss': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'dashboard.blogpost': {
            'Meta': {'object_name': 'BlogPost', '_ormbases': ['dashboard.Event']},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Blog']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dashboard.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'markdown': ('django.db.models.fields.TextField', [], {})
        },
        'dashboard.commit': {
            'Meta': {'object_name': 'Commit', '_ormbases': ['dashboard.Event']},
            'diff': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dashboard.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Repository']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'dashboard.contributor': {
            'Meta': {'object_name': 'Contributor'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Project']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'dashboard.event': {
            'Meta': {'object_name': 'Event'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'from_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Project']", 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'})
        },
        'dashboard.project': {
            'Meta': {'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'blog': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dashboard.Blog']", 'unique': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repository': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dashboard.Repository']", 'unique': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'wiki': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'dashboard.repository': {
            'Meta': {'object_name': 'Repository'},
            'clone_url': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'cmd': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'from_feed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'most_recent_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'repo_rss': ('django.db.models.fields.URLField', [], {'max_length': '128'}),
            'vcs': ('django.db.models.fields.CharField', [], {'default': "'git'", 'max_length': '3'}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '128'})
        },
        'dashboard.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'dashboard.share': {
            'Meta': {'object_name': 'Share', '_ormbases': ['dashboard.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dashboard.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'external_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link_display': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboard']
