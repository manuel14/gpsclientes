from django.shortcuts import render
from .models import Cliente
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json


def index(request):
    clientes = Cliente.objects.all().order_by('clientenro')
    page = request.GET.get('page')
    total = len(clientes)
    paginator = Paginator(clientes, 10)
    cant_pend = Cliente.objects.filter(latitud_22172__isnull=True).count()
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
        cli.latitud_4326 = float(lat_4326)
        cli.longitud_4326 = float(lon_4326)
        cli.latitud_22172 = float(lat_22172)
        cli.longitud_22172 = float(lon_22172)
        cli.precision = precision
        cli.fecha_posicion = datetime.now()
        cli.save()
        if edif_flag == "true":
            clientes = Cliente.objects.filter(
                direccion=cli.direccion)
            for c in clientes:
                c.latitud_4326 = float(lat_4326)
                c.longitud_4326 = float(lon_4326)
                c.latitud_22172 = float(lat_22172)
                c.longitud_22172 = float(lon_22172)
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
        all_objects = Cliente.objects.filter(Q(latitud_22172__isnull=True) &
                                             Q(direccion__icontains=global_search)
                                             | Q(clientenro__icontains=global_search)
                                             | Q(nombre__icontains=global_search)
                                             )
    else:
        all_objects = Cliente.objects.filter(latitud_22172__isnull=True)
    columns = ['clientenro', 'nombre', 'direccion', 'posicion', 'edificio']
    objects = []

    for i in all_objects.order_by('clientenro')[start:start + length].values():
        clientenro = str(i["clientenro"])
        html_pos = "<button type=""button"" id=""{0}"" value=""{0}"" class=""{1}"">Obtener Posición</button>".format(
            clientenro, " btn")
        html_edif = "<div id=""edif"" class=""form-check""><label class=""form-check-label""><input class=""form-check-input"" type=""checkbox"" value=""{0}"">Es edificio</label></div>".format(
            clientenro)
        ret = [i[j] if j not in ['posicion', 'edificio']
               else html_pos if j == 'posicion' else html_edif for j in columns]
        objects.append(ret)
    filtered_count = all_objects.count()
    total_count = Cliente.objects.all().count()
    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": objects,
    })


def error404(request):
    return render(request, 'web/404.html')


def error500(request):
    return render(request, 'web/500.html')


def completados(request):
    clientes = Cliente.objects.all().order_by('clientenro')
    cant_comp = Cliente.objects.filter(latitud_22172__isnull=False).count()
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
        all_objects = Cliente.objects.filter(Q(latitud_22172__isnull=False) &
                                             Q(direccion__icontains=global_search)
                                             | Q(clientenro__icontains=global_search)
                                             | Q(nombre__icontains=global_search)
                                             )
    else:
        all_objects = Cliente.objects.filter(latitud_22172__isnull=False)
    columns = ['clientenro', 'nombre', 'direccion', 'posicion']
    objects = []

    for i in all_objects.order_by('clientenro')[start:start + length].values():
        clientenro = str(i["clientenro"])
        html_pos = "<button type=""button"" id=""{0}"" value=""{0}"" class=""{1}"">Obtener Posición</button>".format(
            clientenro, "btn")
        ret = [i[j] if j != "posicion"
               else html_pos for j in columns]
        objects.append(ret)
    filtered_count = all_objects.count()
    total_count = Cliente.objects.all().count()
    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": objects,
    })


def tracking(request):
    completados = Cliente.objects.filter(latitud_4326__isnull=False).values_list(
        'latitud_4326',
        'longitud_4326',
        'nombre',
        'fecha_posicion',
        'direccion',
        'clientenro'
    )
    return render(request, 'web/map.html',
                  {'clientes': json.dumps(list(completados), cls=DjangoJSONEncoder)})
