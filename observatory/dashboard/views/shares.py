from dashboard.models import BlogPost, Blog
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from observatory.dashboard.views import blogs

def show_item(request, id):
  post = get_object_or_404(BlogPost, id = id)
  if not post.from_feed:
    return HttpResponseRedirect(reverse(blogs.show_post,
                                          args = (post.project.url_path,
                                                  post.url_path,)))
  else:
    return render_to_response('shares/shares.html', {
        'post': post
      }, context_instance = RequestContext(request))