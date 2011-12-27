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

from django import template
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from observatory.settings import HEADER_TEMPLATE, FAVICON_PATH
from dashboard.models import Contributor, NotificationRead


register = template.Library()

###
#   Used so page header template can be defined in settings for customization.
###
def pageheader():
  return render_to_string(HEADER_TEMPLATE)

register.simple_tag(pageheader)


###
#   Used so favicon path can be defined in settings for customization
###
def favicon():
  if FAVICON_PATH:
    return '<link rel="shortcut icon" href="'+FAVICON_PATH+'" />'

register.simple_tag(favicon)

def karma(userid):
	"""Returns karma in the form of (x)
	"""
	try:
		contributor = Contributor.objects.get(user=userid)
	except:
		return ""
	return "(%d)" % contributor.karma

register.simple_tag(karma)

def notifications(userid):
	try:
		notify = NotificationRead.objects.get(user=userid)
	except:
		return "0"
	return notify.unread

register.simple_tag(notifications)