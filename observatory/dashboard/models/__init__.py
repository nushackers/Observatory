# Copyright (c) 2010, individual contributors (see AUTHORS file)
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from AuthorRequest import AuthorRequest
from Blog import Blog
from BlogPost import BlogPost
from Commit import Commit
from Contributor import Contributor
from Event import Event
from EventSet import EventSet
from Notification import Notification, NotificationRead
from Project import Project
from Repository import Repository
from Screenshot import Screenshot
from Share import Share
from URLPathedModel import URLPathedModel

# Signals

import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from threadedcomments.models import ThreadedComment


def denormalize_comments(sender, instance, created=False, **kwargs):
  """This receiver denormalizes comments to the event model.
  Used whenever a comment is saved. Purpose: to keep front-page load times down.
  """
  event_type = ContentType.objects.get_for_model(instance.content_object)
  instance.content_object.num_comments = instance.content_object.get_num_comments(event_type.id)
  instance.content_object.save()

def create_notification(sender, instance, created, **kwargs):
  """This receiver creates notifications whenever a comment is saved
  """
  if created:
    parent = instance.content_object
    # Some Events don't have authors. In such cases, no need to create notifications.
    try:
      user = parent.author
    except:
      user = None

    if user:
      parent_comment = instance.parent
      notify_type = "comment" if parent_comment else parent.type_name().lower()
      notify = Notification(
            user = user,
            author = instance.user,
            content_object = parent,
            time = datetime.datetime.utcnow(),
            notification_type = notify_type)
      notify.save()

models.signals.post_save.connect(denormalize_comments, sender=ThreadedComment)
models.signals.post_delete.connect(denormalize_comments, sender=ThreadedComment)
models.signals.post_save.connect(create_notification, sender=ThreadedComment, dispatch_uid="37cce9dce88")
