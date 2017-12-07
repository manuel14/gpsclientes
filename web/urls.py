from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^position/$', views.position, name="position"),
    url(r'^clientestable/$', views.clientestable, name="clientestable"),
]
