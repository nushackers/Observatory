# Notifications are needed for user engagement.

from dashboard.util import time_ago
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from BlogPost import BlogPost
from Commit import Commit
from Share import Share

class Notification(models.Model):
  class Meta:
    app_label = 'dashboard'

  # user is to be notified
  user = models.ForeignKey(User, related_name="notification_user")
  # author that 'created' the notification
  author = models.ForeignKey(User, related_name="notification_author")
  # time created
  time = models.DateTimeField()
  # generic content type
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')

  notification_type = models.CharField(max_length = 64)

  def __unicode__(self):
    return u'Notification of type %s' % self.notification_type

class NotificationRead(models.Model):
  """Records when user last read notifications
  """
  class Meta:
    app_label = 'dashboard'
  user = models.ForeignKey(User)
  lasttime_read = models.DateTimeField()

  def __unicode__(self):
    return u'Notification Last Read Object'