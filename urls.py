from django.conf.urls.defaults import *
from django.conf import settings

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'watcher.views.index', name='watcher_index'),
    url(r'^user/(?P<username>.+)/$', 'watcher.views.user_index', name='watcher_user_index'),
    url(r'^user_logged_in_redirect/$', 'watcher.views.user_logged_in_redirect', name='watcher_user_logged_in_redirect'),
    url(r'^log/(?P<access_key>[a-z0-9]{32})/$', 'watcher.views.log_article_user', name='watcher_log_article_user'),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
