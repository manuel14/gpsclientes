from django.contrib import admin
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
	ordering = ('clientenro', )

# Register your models here.
admin.site.register(Cliente, ClienteAdmin)

