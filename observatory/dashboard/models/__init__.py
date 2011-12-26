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
from Project import Project
from Repository import Repository
from Screenshot import Screenshot
from Share import Share
from URLPathedModel import URLPathedModel

"""The following signal denormalizes comments to the event model.
Used whenever a comment is saved. Purpose: to keep front-page load times down.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from threadedcomments.models import ThreadedComment

def denormalize_comments(sender, instance, created=False, **kwargs):
  event_type = ContentType.objects.get_for_model(instance.content_object)
  instance.content_object.num_comments = instance.content_object.get_num_comments(event_type.id)
  instance.content_object.save()

models.signals.post_save.connect(denormalize_comments, sender=ThreadedComment)
models.signals.post_delete.connect(denormalize_comments, sender=ThreadedComment)

"""Create a Contributor object upon user registration
"""
from django.contrib.auth.models import User
def create_contributor(sender, instance, created, **kwargs):
  if created:
    try:
      cont = Contributor.objects.get(email=instance.email)
    except:
      cont = Contributor(user=instance,
                     name=instance.first_name + " " + instance.last_name,
                     email=instance.email)
      cont.save()

# Dispatcher is hashed, used for preventing duplicate signals
models.signals.post_save.connect(create_contributor,
          sender=User,
          dispatch_uid="275ba354958cdce88")
