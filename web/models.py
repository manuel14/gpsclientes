from django.db import models


class Nodo(models.Model):
    numero = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.numero


class Barrio(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    nodo = models.ForeignKey(Nodo, related_name="barrios",
                             on_delete=None, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Calle(models.Model):
    nombre = models.CharField(max_length=200)
    geocode = models.BooleanField(default=False)
    osm_geocode = models.NullBooleanField()
    calleidsiga = models.IntegerField()
    limite_inferior = models.IntegerField(blank=True, null=True)
    limite_superior = models.IntegerField(blank=True, null=True)
    calle_chica = models.NullBooleanField()

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    tira = models.CharField(max_length=20, blank=True, null=True)
    piso = models.CharField(max_length=20, blank=True, null=True)
    depto = models.CharField(max_length=20, blank=True, null=True)
    barrio = models.ForeignKey(
        Barrio, related_name="clientes", blank=True, null=True, on_delete=None)
    latitud_4326 = models.FloatField(null=True, blank=True)
    longitud_4326 = models.FloatField(null=True, blank=True)
    latitud_22172 = models.FloatField(null=True, blank=True)
    longitud_22172 = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    fecha_posicion = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    clientenro = models.IntegerField(unique=True)
    geocode = models.BooleanField(default=False)
    calle = models.ForeignKey(Calle, blank=True,
                              null=True, on_delete=models.SET_NULL, related_name="clientes")
    puerta = models.IntegerField(blank=True, null=True)
    clicalubicacion = models.CharField(max_length=200, null=True, blank=True)
    P = "P"
    C = "C"
    X = "X"
    B = "B"
    K = "K"
    E = "E"
    M = "M"
    A = "A"
    estado_choices = (
        (P, 'Pendiente'),
        (C, 'Conectado'),
        (X, 'Desconectado'),
        (B, "Ingresado"),
        (E, 'liquidado'),
        (M, 'Baja Moroso'),
        (A, 'Anulado'),
        (K,'Cortado')
    )
    estado = models.CharField(
        max_length=20, choices=estado_choices, default=C)
    nodo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.clientenro)
