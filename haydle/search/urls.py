from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^search/(?P<query>\w+)$', 'haydle.search.views.index'),
    (r'^$', 'haydle.search.views.index'),
)

