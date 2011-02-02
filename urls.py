from django.conf.urls.defaults import *
from django.conf import settings

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^add_link/$', 'watcher.views.add_link', name='watcher_add_link'),
    
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

