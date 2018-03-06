from web.models import Cliente, Calle
from django.db.models import Max
from sigabd import sigabdConnector
from . sigacredentials import USER, PASS
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging

logger = logging.getLogger(__name__) 

def complete_clientes():
	maximo = Cliente.objects.all().aggregate(Max('clientenro'))["clientenro__max"]
	con = sigabdConnector(USER, PASS)
	result = con.complete_clientes(maximo)
	logger.info(len(result))
	clientes = []
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
		clientes.append(c)
	Cliente.objects.bulk_create(clientes)
	return HttpResponse(status=200)


