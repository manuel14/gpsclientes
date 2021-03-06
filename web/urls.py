from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^completados', views.completados, name="completados"),
    url(r'^position/$', views.position, name="position"),
    url(r'^clientestable/$', views.clientestable, name="clientestable"),
    url(r'^table_completados/$', views.table_completados, name="table_completados"),
    url(r'^tracking/$', views.tracking, name="tracking"),
    url(r'^form_tracking/$', views.form_tracking, name="form_tracking"),
    url(r'^geocoder/$', views.geocoder, name="geocoder"),
    url(r'^clientes_geocode/$', views.clientes_geocode, name="clientes_geocode"),
    url(r'^convert_22172/$', views.convert_22172, name="convert_22172"),
    url(r'^save_22172/$', views.save_22172, name="save_22172"),
    url(r'^ubicados/$', views.ubicados, name="ubicados"),
    url(r'^form_ubicados/$', views.form_ubicados, name="form_ubicados"),
    url(r'^calle_cliente/$', views.calle_for_cliente, name="calle_cliente"),
    url(r'^update_direccion/$', views.update_direccion, name="update_direccion"),
    url(r'^osm_geocode/$', views.osm_geocode, name="osm_geocode"),
]
