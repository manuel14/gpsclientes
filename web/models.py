from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    fecha_posicion = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    clientenro = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.clientenro)
