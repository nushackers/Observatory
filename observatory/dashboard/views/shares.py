import datetime
from urlparse import urlparse
from dashboard.models import BlogPost, Share
from observatory.dashboard.views import blogs, feed
from dashboard.forms import ShareForm
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from lib.markdown import markdown

def show_post(request, id):
  post = get_object_or_404(BlogPost, id = id)
  if not post.from_feed:
    return HttpResponseRedirect(reverse(blogs.show_post,
                                          args = (post.project.url_path,
                                                  post.url_path,)))
  else:
    return render_to_response('shares/shares.html', {
        'post': post
      }, context_instance = RequestContext(request))

def show_link(request, id):
  share = get_object_or_404(Share, id = id)
  return render_to_response('shares/shares.html', {
        'post': share
      }, context_instance = RequestContext(request))

def redirect_link(request, id):
  share = get_object_or_404(Share, id = id)
  if share.external_link:
    return HttpResponseRedirect(share.external_link)
  else:
    return HttpResponseRedirect(reverse(show_link, args = (id,)))

@login_required
def create_share(request):
  form = ShareForm(request.POST)

  if form.is_valid():
    if request.POST['title'] and not request.POST['summary'] and not request.POST['external_link']:
        # Don't let people create posts with only a title
        return HttpResponseRedirect(reverse(feed.main))
    tld = urlparse(request.POST['external_link']).netloc if request.POST['external_link'] else None
    date = datetime.datetime.utcnow()
    text = markdown(request.POST['summary'], safe_mode = True)
    share = Share(title = request.POST['title'],
                  external_link = request.POST['external_link'],
                  summary = text,
                  from_feed = False,
                  author = request.user,
                  date = date)
    if tld:
      share.link_display = tld
    share.save()
    return HttpResponseRedirect(reverse(feed.main))
  else:
    return render_to_response('shares/shareform.html', {
      'form': form
    }, context_instance = RequestContext(request))

