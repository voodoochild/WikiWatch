from django.conf.urls.defaults import *
from django.conf import settings

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'watcher.views.index', name='watcher_index'),
    url(r'^log_article/(?P<access_key>[a-z0-9]{32})/$', 'watcher.views.log_article_user', name='watcher_log_article_user'),
    url(r'^log_article/$', 'watcher.views.log_article', name='watcher_log_article'),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
