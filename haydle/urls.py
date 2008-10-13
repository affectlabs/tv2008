from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^', include('haydle.search.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
