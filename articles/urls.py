from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^press-release/(?P<pk>[0-9]+)/$', views.PressReleaseDetailView.as_view(), name='press-release-detail'),
    url(r'add/$', views.PressReleaseCreate.as_view(), name='press-release-add'),
    url(r'edit/(?P<pk>[0-9]+)/$', views.PressReleaseUpdate.as_view(), name='press-release-update'),
    url(r'delete/(?P<pk>[0-9]+)/$', views.PressReleaseDelete.as_view(), name='press-release-delete'),
]