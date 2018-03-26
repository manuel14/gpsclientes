from web.models import Cliente, Calle, Nodo
from django.db.models import Max
from sigabd import sigabdConnector
from . sigacredentials import USER, PASS
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import IntegrityError
import logging
import json

logger = logging.getLogger(__name__)


def complete_clientes():
    maximo = Cliente.objects.all().aggregate(
        Max('clientenro'))["clientenro__max"]
    con = sigabdConnector(USER, PASS)
    result = con.complete_clientes(maximo)
    logger.info(len(result))
    for r in result:
        try:
            ca = Calle.objects.get(calleidsiga=r["calleidsiga"])
        except ObjectDoesNotExist:
            ca = Calle(
                calleidsiga=r["calleidsiga"],
                nombre=r["callenombre"]
            )
            ca.save()
        except MultipleObjectsReturned:
            logger.info(r["calleidsiga"])
            continue
        try:
            puerta = int(r["puerta"])
        except (ValueError, TypeError):
            puerta = None
        c = Cliente(
            clientenro=r["clientenro"], nombre=r["nombre"],
            clicalubicacion=r["ubicacion"], piso=r["piso"],
            depto=r["depto"], estado=r["estado"],
            puerta=puerta, calle=ca
        )
        try:
            c.save()
        except IntegrityError:
            logger.info(c.clientenro)
            continue
        if puerta:
            c.direccion = ca.nombre + " " + str(puerta)
        else:
            c.direccion = ca.nombre
        c.save()
    return HttpResponse(status=200)


"""Método que actualiza estado, calle,puerta y nodo trayendo la info desde siga
    Informa la cantidad de actualizados contra el total
"""


def update_pendientes():
    clientes = Cliente.objects.filter(latitud_4326__isnull=True)
    con = sigabdConnector(USER, PASS)
    cont = 0
    for cli in clientes:
        dire = con.get_calle_for_cliente(cli.clientenro)
        estado = con.get_estado_for_cliente(cli.clientenro)
        nodo = con.get_nodo_for_cliente(cli.clientenro)
        nodo = nodo["zonaid"]
        try:
            if int(dire["puerta"]) != cli.puerta:
                cli.puerta = int(dire["puerta"])
                cli.save()
            if dire["calleidsiga"] != cli.calle.calleidsiga:
                cli.calle = Calle.object.get(calleidsiga=dire["calleidsiga"])
                cli.save()
        except (TypeError, AttributeError, ValueError):
            pass
        logger.info(estado)
        if estado != cli.estado:
            cli.estado = estado
            cli.save()
        logger.info(nodo)
        if cli.nodo != nodo:
            cli.nodo = nodo
            cli.save()
        cont += 1
    logger.info("actualizados: " + str(cont) + "total: " + str(len(clientes)))
    return True


"""Carga de nodo a todos los clientes de la bd"""


def cargar_nodo():
    clientes = Cliente.objects.filter(nodo__isnull=True)
    cont = 0
    con = sigabdConnector(USER, PASS)
    for c in clientes:
        nodo_info = con.get_nodo_for_cliente(c.clientenro)
        if nodo_info:
            try:
                nodo = Nodo.objects.get(zonaid=nodo_info["zonaid"])
                c.nodo_fk = nodo
                c.save()
                cont += 1
            except ObjectDoesNotExist:
                continue
        else:
            continue
    logger.info("act: " + str(cont))
    return True


def llenar_tabla_nodo():
    con = sigabdConnector(USER, PASS)
    nodos = con.get_nodos()
    nodos_lista = []
    for n in nodos:
        nodo_obj = Nodo(
            nombre=n["zonanombre"],
            zonaid=n["zonaid"]
        )
        nodos_lista.append(nodo_obj)
    Nodo.objects.bulk_create(nodos_lista)
    return True
