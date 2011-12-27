import datetime
from dashboard.models import (
  BlogPost,
  Commit,
  Share,
  Notification,
  NotificationRead
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

NOTIFY_PER_PAGE = 30

@login_required
def view_notify(request):
  """Shows unread notifications, and the first page of read ones.
  """
  notify = Notification.objects.filter(user=request.user).order_by('time').reverse()
  read = NotificationRead.objects.get(user=request.user)
  # split into unread and read
  unread_ls = notify.filter(time__gt = read.lasttime_read)
  print unread_ls
  paginator = Paginator(notify.filter(time__lte = read.lasttime_read),
                        NOTIFY_PER_PAGE)

  page = paginator.page(1)

  # save read time as now
  read.lasttime_read = datetime.datetime.utcnow()
  read.unread = 0
  read.save()
  return render_to_response('partials/notifications.html', {
    'unread_ls': unread_ls,
    'read_ls': page,
    'disable_content': True
  }, context_instance = RequestContext(request))

@login_required
def view_notify_page(request, page_num):
  if page_num == 1:
    return HttpResponseRedirect(reverse(view_notify))

  read = NotificationRead.objects.get(user=request.user)
  paginator = Paginator(Notification.objects.filter(user=request.user).exclude(time__gt = read.lasttime_read).order_by('time').reverse(),
        NOTIFY_PER_PAGE)

  if int(page_num) not in paginator.page_range:
    raise Http404

  page = paginator.page(page_num)

  return render_to_response('partials/notifications.html', {
    'read_ls': page,
    'disable_content': True
  }, context_instance = RequestContext(request))