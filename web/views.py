from django.shortcuts import render
from .models import Cliente, Calle
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from sigabd import sigabdConnector
from .sigacredentials import USER, PASS
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
import json
import googlemaps
import logging
import time
import requests

logger = logging.getLogger(__name__)


def index(request):
    clientes = Cliente.objects.filter(estado='C').order_by('clientenro')
    page = request.GET.get('page')
    total = len(clientes)
    paginator = Paginator(clientes, 10)
    cant_pend = Cliente.objects.filter(latitud_4326__isnull=True, estado='C').count()
    try:
        clientes_pags = paginator.page(page)
    except PageNotAnInteger:
        clientes_pags = paginator.page(1)
    except EmptyPage:
        clientes_pags = paginator.page(paginator.num_pages)

    return render(request, 'web/index.html', {
        "clientes": clientes_pags, "cant_pend": cant_pend,
        "total": total})


def position(request):
    lat_4326 = request.POST.get("latitud_4326", None)
    lat_22172 = request.POST.get("latitud_22172", None)
    lon_4326 = request.POST.get("longitud_4326", None)
    lon_22172 = request.POST.get("longitud_22172", None)
    precision = request.POST.get("precision", None)
    clientenro = request.POST.get("clientenro", None)
    edif_flag = request.POST.get("edif_flag", None)
    if lat_22172 and lon_22172 and clientenro and precision:
        cli = Cliente.objects.get(clientenro=clientenro)
        cli.latitud_4326 = round(float(lat_4326), 2)
        cli.longitud_4326 = round(float(lon_4326), 2)
        cli.latitud_22172 = round(float(lat_22172), 2)
        cli.longitud_22172 = round(float(lon_22172), 2)
        cli.precision = precision
        cli.fecha_posicion = datetime.now()
        cli.save()
        if edif_flag == "true":
            clientes = Cliente.objects.filter(Q(
                direccion=cli.direccion) & Q(tira=cli.tira) | Q(direccion=cli.direccion))
            for c in clientes:
                c.latitud_4326 = round(float(lat_4326), 2)
                c.longitud_4326 = round(float(lon_4326), 2)
                c.latitud_22172 = round(float(lat_22172), 2)
                c.longitud_22172 = round(float(lon_22172), 2)
                c.precision = precision
                c.fecha_posicion = datetime.now()
                c.save()
        return HttpResponse(status=200)


def clientestable(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    global_search = request.GET['search[value]']
    if global_search:
        all_objects = Cliente.objects.filter(Q(latitud_4326__isnull=True)& 
                                              (Q(estado='C'))&
                                             (Q(direccion__icontains=global_search)
                                              | Q(clientenro__icontains=global_search)
                                              | Q(nombre__icontains=global_search)
                                              | Q(tira__icontains=global_search)
                                              | Q(piso__icontains=global_search)
                                              | Q(depto__icontains=global_search)
                                              ))
    else:
        all_objects = Cliente.objects.filter(latitud_4326__isnull=True, estado='C')
    columns = ['clientenro', 'nombre', 'direccion', 'posicion', 'edificio']
    objects = []

    for i in all_objects.order_by('clientenro')[start:start + length].values():
        clientenro = str(i["clientenro"])
        html_pos = "<button type=""button"" id=""{0}"" value=""{0}"" class=""{1}"">Obtener Posición</button>".format(
            clientenro, " btn")
        html_edif = "<div id=""edif"" class=""form-check""><label class=""form-check-label""><input class=""form-check-input"" type=""checkbox"" value=""{0}"">Es edificio</label></div>".format(
            clientenro)
        dire = i["direccion"] + " "
        if i["tira"] and i["tira"].strip() != "":
            dire += "tira:" + i["tira"].strip()
        else:
            if i["clicalubicacion"]:
                dire += " " + i["clicalubicacion"]
        ret = [i[j] if j not in ['direccion', 'posicion', 'edificio']
               else dire if j == 'direccion' else html_pos if j == 'posicion' else html_edif for j in columns]
        objects.append(ret)
    filtered_count = all_objects.count()
    total_count = Cliente.objects.filter(estado='C').count()
    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": objects,
        "order": [[2, 'desc']],
        "orderable": [2, True]
    })


def error404(request):
    return render(request, 'web/404.html')


def error500(request):
    return render(request, 'web/500.html')


def completados(request):
    clientes = Cliente.objects.filter(estado='C').order_by('clientenro')
    cant_comp = Cliente.objects.filter(latitud_4326__isnull=False, estado='C').count()
    total = len(clientes)
    page = request.GET.get('page')
    paginator = Paginator(clientes, 10)
    try:
        clientes_pags = paginator.page(page)
    except PageNotAnInteger:
        clientes_pags = paginator.page(1)
    except EmptyPage:
        clientes_pags = paginator.page(paginator.num_pages)

    return render(request, 'web/completados.html', {
        "clientes": clientes_pags, "cant_comp": cant_comp,
        "total": total})


def table_completados(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    global_search = request.GET['search[value]']
    if global_search:
        all_objects = Cliente.objects.filter(Q(latitud_4326__isnull=False) & 
                                            (Q(estado='C')) &                                
                                            (Q(direccion__icontains=global_search)
                                             | Q(clientenro__icontains=global_search)
                                             | Q(nombre__icontains=global_search)
                                             | Q(tira__icontains=global_search)
                                             | Q(piso__icontains=global_search)
                                             | Q(depto__icontains=global_search)
                                             ))
    else:
        all_objects = Cliente.objects.filter(latitud_4326__isnull=False, estado='C')
    columns = ['clientenro', 'nombre', 'direccion', 'posicion']
    objects = []

    for i in all_objects.order_by('clientenro')[start:start + length].values():
        clientenro = str(i["clientenro"])
        html_pos = "<button type=""button"" id=""{0}"" value=""{0}"" class=""{1}"">Obtener Posición</button>".format(
            clientenro, "btn")
        dire = i["direccion"] + " "
        if i["tira"] and i["tira"].strip() != "":
            dire += "tira:" + i["tira"]
        else:
            if i["clicalubicacion"]:
                dire += " " + i["clicalubicacion"]
        ret = [i[j] if j not in ["posicion", 'direccion']
               else html_pos if j == 'posicion' else dire for j in columns]
        objects.append(ret)
    filtered_count = all_objects.count()
    total_count = Cliente.objects.filter(estado='C').count()
    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": objects,
        "order": [[2, 'desc']]
    })


def tracking(request):
    fecha = request.GET.get("fecha", None)
    date = datetime.strptime(fecha, "%Y-%m-%d")
    completados = Cliente.objects.filter(
        latitud_4326__isnull=False, fecha_posicion__date=date
    ).values_list(
        'latitud_4326',
        'longitud_4326',
        'nombre',
        'fecha_posicion',
        'direccion',
        'clientenro'
    )
    return render(request, 'web/map.html',
                  {'clientes': json.dumps(list(completados), cls=DjangoJSONEncoder)})


def form_tracking(request):
    return render(request, 'web/tracking.html')


def geocoder(request):
    clientes = Cliente.objects.filter(geocode=True)
    return render(request, 'web/geocoder.html', {"clientes": clientes})


def calle_for_cliente(request):
    clientes = Cliente.objects.filter(calle__isnull=True,
                                      latitud_4326__isnull=True).values_list(
        "clientenro", flat=True)
    con = sigabdConnector(USER, PASS)
    for c in clientes:
        cli = Cliente.objects.get(clientenro=c)
        result = con.get_calle_for_cliente(c)
        if result:
            try:
                puerta = int(result["puerta"])
            except ValueError:
                continue
            calleid = result["calleidsiga"]
            try:
                calle = Calle.objects.get(calleidsiga=calleid)
                cli.calle = calle
                cli.puerta = puerta
                cli.save()
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                continue
        else:
            continue
    return HttpResponse(status=200)


def clientes_geocode(request):
    clientes = Cliente.objects.filter(
        (Q(puerta__isnull=False) &
         Q(latitud_4326__isnull=True) &
         Q(longitud_4326__isnull=True) &
         Q(calle__limite_inferior__lte=F('puerta')) &
         Q(calle__limite_superior__gte=F('puerta'))&
         Q(calle__geocode=True)
         )
        | (Q(latitud_4326__isnull=True) &
           Q(longitud_4326__isnull=True) &
            Q(calle__calle_chica=True) &
            Q(puerta__isnull=False) &
            Q(calle__isnull=False) &
            Q(calle__geocode=True))
    )
    gclient = googlemaps.Client(key='AIzaSyDqZBSnWiaoZsTxIbQjaNcM2xXuXk2IPv4',
                                )
    no_ubicables = []
    ubicados = 0
    for c in clientes:
        dire = c.calle.nombre + " " + \
            str(c.puerta) + ",ushuaia,tierra del fuego"
        coords = gclient.geocode(address=dire)
        if coords == []:
            no_ubicables.append({"clientenro": c.clientenro})
            continue
        else:
            ubicados += 1
            c.latitud_4326 = coords[0]["geometry"]["location"]["lat"]
            c.longitud_4326 = coords[0]["geometry"]["location"]["lng"]
            c.save()
        time.sleep(1)
    with open("no_ubicables.txt", "w")as outfile:
        json.dump(no_ubicables, outfile, ensure_ascii=False)
    logger.info("ubicados: " + str(ubicados))

    return HttpResponse(status=200)


def convert_22172(request):
    clientes = Cliente.objects.filter(
        latitud_22172__isnull=True,
        latitud_4326__isnull=False)[:500].values_list("clientenro", "latitud_4326", "longitud_4326")
    clientes = json.dumps(list(clientes))
    return render(request, 'web/convert.html', {"clientes": clientes})


def save_22172(request):
    clientes = json.loads(request.POST.get("clientes", None))
    if clientes:
        for c in clientes:
            cli = Cliente.objects.get(clientenro=c["clientenro"])
            cli.latitud_22172 = c["latitud_22172"]
            cli.longitud_22172 = c["longitud_22172"]
            cli.save()
    else:
        return HttpResponse(status=400)
    return HttpResponse(status=200)


def form_ubicados(request):
    return render(request, 'web/form_ubicados.html')


def ubicados(request):
    clientes = Cliente.objects.filter(latitud_4326__isnull=False).values_list(
        "latitud_4326", "longitud_4326", "clientenro", "nombre", "direccion",)
    return render(request, 'web/map.html',
                  {'clientes': json.dumps(list(clientes), cls=DjangoJSONEncoder)})


@csrf_exempt
def update_direccion(request):
    lista = json.loads(request.body)
    clientes = Cliente.objects.filter(clientenro__in=lista)
    con = sigabdConnector(USER, PASS)
    cont = 0
    for c in clientes:
        try:
            direccion = con.get_direccion_for_cliente(c.clientenro)
            if direccion["puerta"].strip() == "":
                continue
            c.direccion = direccion["calle"] + direccion["puerta"]
            c.tira = direccion["tira"]
            c.piso = direccion["piso"]
            c.depto = direccion["depto"]
            c.clicalubicacion = direccion["clicalubicacion"]
            c.save()
            cont += 1
        except (ObjectDoesNotExist, ValueError):
            continue
    logger.info("total:" + str(cont))
    return HttpResponse(status=200)


def osm_geocode(request):
    clientes = Cliente.objects.filter(
        calle__osm_geocode=True,
        calle__calle_chica=True,
        latitud_4326__isnull=True,
        longitud_4326__isnull=True
    )[:10]
    url = "https://nominatim.openstreetmap.org/"
    url += "?format=json"
    cont = 0
    no_ubicados = []
    for c in clientes:
        try:
            url += "&street=%s" % c.calle.nombre + " " + str(c.puerta)
        except ValueError:
            continue
        url += "&city=ushuaia&country=argentina&limit=1"
        r = requests.get(url)
        if r.status_code == 200 and r.json() != []:
            coords = r.json()[0]
            c.latitud_4326 = coords["lat"]
            c.longitud_4326 = coords["lon"]
            c.save()
            cont += 1
        else:
            no_ubicados.append({"clientenro": c.clientenro,
                                "direccion": c.calle.nombre})
    logger.info("ubicados:" + str(cont))
    json_out = json.dumps(no_ubicados)
    return JsonResponse(json_out, safe=False)
