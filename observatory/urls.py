from dashboard.feeds import *
from dashboard.models import *
from dashboard.views import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User, Group
from voting.views import xmlhttprequest_vote_on_object
from threadedcomments.models import ThreadedComment
from django.conf.urls.defaults import *
import settings
from voting.models import Vote

from django.contrib import admin

# autodiscover doesn't work, do it manually
for model in (AuthorRequest,
              Blog,
              BlogPost,
              Commit,
              Contributor,
              Event,
              Project,
			  User,
			  Group,
              Vote,
              ThreadedComment,
              Repository,
              Screenshot,
              Share):
     admin.site.register(model)

urlpatterns = patterns('',
    # Example:
    # (r'^observatory/', include('observatory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # author requests
    (r'^author-request/approve/(\d+)/$', author_requests.approve),
    (r'^author-request/reject/(\d+)/$', author_requests.reject),

    # blog posts
    (r'^posts/add/(\d+)/$', blogs.write_post),
    (r'^posts/create/(\d+)/$', blogs.create_post),
    (r'^posts/page/(\d+)/$', blogs.posts_page),
    (r'^project/([^\.]*)/post/([^\.]*)/modify/$', blogs.edit_post),
    (r'^project/([^\.]*)/post/([^\.]*)/update/$', blogs.update_post),
    (r'^project/([^\.]*)/post/([^\.]*)/delete/$', blogs.delete_post),
    (r'^project/([^\.]*)/post/([^\.]*)/$', blogs.show_post),
    (r'^post/([^\.]*)/$', blogs.show_user_post),
    (r'^project/([^\.]*)/post/([^\.]*)\.rss$',
     SingleFeed(),  {'model': BlogPost}),

    (r'^projects/([^\.]*)/posts/$', blogs.show_blog),
    (r'^projects/([^\.]*)/posts\.rss$', BlogPostsFeed()),

    (r'^posts/$', blogs.posts),
    (r'^posts\.rss$', BlogPostsFeed()),

    # notifications
    (r'^notifications/$', notifications.view_notify),
    (r'^notifications/page/(\d+)/$', notifications.view_notify_page),

    # shares
    (r'^share/create/$', shares.create_share),
    (r'^share/post/([^\.]*)/$', shares.show_post),
    (r'^share/link/([^\.]*)/$', shares.show_link),
    (r'^share/redirect/(?P<sharetype>link|post)/(?P<id>[^\.]*)/$', shares.redirect_link),

    # users
    (r'^register-or-login/$', users.login_or_reg),
    (r'^register/$', users.register),
    (r'^login/$', users.login),
    (r'^logout/$', users.logout),
    (r'^user/(\d+)/commits/$', commits.show_user),
    (r'^user/(\d+)/posts/personal/remove/$', blogs.remove_personal_blog),
    (r'^user/(\d+)/posts/personal/$', blogs.edit_personal_blog),
    (r'^user/(\d+)/post/([^\.]*)/$', blogs.show_user_post),
    (r'^user/(\d+)/posts/$', blogs.show_user_blog),
    (r'^user/(\d+)/$', users.profile),
    (r'^people/$', users.people),
	(r'^past_people/$', users.past_people),
	(r'^user_deactivate/(\d+)/$', users.deactivate),
	(r'^user_activate/(\d+)/$', users.activate),
    (r'^forgot-password/$', users.forgot_password),
    (r'^forgot_password_success/$', users.forgot_password_success),

    # commits
    (r'^projects/([^\.]*)/commit/([^\.]*)/$', commits.show),
    (r'^projects/([^\.]*)/commit/([^\.]*)\.rss$',
     SingleFeed(), {'model': Commit}),

    (r'^commits/(\d+)/$', commits.all_page),
    (r'^commits/$', commits.all),
    (r'^commits\.rss$', CommitsFeed()),

    (r'^projects/([^\.]*)/commits/$', commits.show_repository),
    (r'^projects/([^\.]*)/commits/(\d+)/$', commits.repository_page),
    (r'^projects/([^\.]*)/commits\.rss$', CommitsFeed()),

    # projects
    (r'^projects/add-user/$', projects.add_user),
    (r'^projects/remove-user/$', projects.remove_user),
    (r'^projects/add/$', projects.add),
    (r'^projects/list/$', projects.list),
    (r'^projects/archive_list/$', projects.archived_list),
    (r'^projects/([^\.]*)/delete-screenshot/(\d+)/$',
        projects.delete_screenshot),
    (r'^projects/([^\.]*)/modify/(\d+)/$', projects.modify),
    (r'^projects/([^\.]*)/modify/$', projects.modify),

    (r'^projects/([^\.]*)/$', projects.show),
    (r'^projects/([^\.]*)\.rss', EventsFeed()),

    (r'^projects/$', projects.list),
    (r'^$', feed.main), #home
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^guidelines/$', direct_to_template, {'template': 'guidelines.html'}),


    # votes
    url(r'^vote/comment/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$',
        votes.xmlhttprequest_vote_on_object,
        { 'model' : ThreadedComment },
        name="vote_on_comment"),

    #comments
    (r'^comments/', include('django.contrib.comments.urls')),

	#tasks
	#(r'^todo/', include('todo.urls')), # Removed tasks from Treehouse

    # feed
    (r'^event/([^\.]*)/$', feed.event),
    #(r'^feed/$', feed.main),
    (r'^feed\.rss$', EventsFeed()),

    # serve media (for now)
    (r'^site-media/(?P<path>.*)/$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

