from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^$', 'haydle.search.views.index'),
)

