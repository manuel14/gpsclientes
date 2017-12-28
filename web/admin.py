from django.contrib import admin
from .models import Cliente, Barrio, Nodo


class ClienteAdmin(admin.ModelAdmin):
    ordering = ('clientenro', )

class BarrioAdmin(admin.ModelAdmin):
	ordering = ('nombre', )

class NodoAdmin(admin.ModelAdmin):
	ordering = ('numero', )

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Nodo, NodoAdmin)
