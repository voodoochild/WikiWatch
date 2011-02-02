from django.conf.urls.defaults import *
from django.conf import settings

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'watcher.views.index', name='watcher_index'),
    url(r'^add_link/$', 'watcher.views.add_link', name='watcher_add_link'),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
