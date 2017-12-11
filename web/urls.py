from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^completados', views.completados, name="completados"),
    url(r'^position/$', views.position, name="position"),
    url(r'^clientestable/$', views.clientestable, name="clientestable"),
    url(r'^table_completados/$', views.table_completados, name="table_completados"),
]
