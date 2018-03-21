from django.contrib import admin
from .models import Cliente, Barrio, Nodo, Calle


class ClienteAdmin(admin.ModelAdmin):
    ordering = ('clientenro', )


class BarrioAdmin(admin.ModelAdmin):
    ordering = ('nombre', )


class NodoAdmin(admin.ModelAdmin):
    ordering = ('zonaid', )


class CalleAdmin(admin.ModelAdmin):
    ordering = ('nombre', )


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Nodo, NodoAdmin)
admin.site.register(Calle, CalleAdmin)
