from django.shortcuts import render
from .models import Cliente
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    clientes = Cliente.objects.all().order_by('clientenro')
    page = request.GET.get('page')
    paginator = Paginator(clientes, 10)
    try:
        clientes_pags = paginator.page(page)
    except PageNotAnInteger:
        clientes_pags = paginator.page(1)
    except EmptyPage:
        clientes_pags = paginator.page(paginator.num_pages)

    return render(request, 'web/index.html', {"clientes": clientes_pags})


def position(request):
    lat = request.POST.get("latitud", None)
    lon = request.POST.get("longitud", None)
    precision = request.POST.get("precision", None)
    clientenro = request.POST.get("clientenro", None)
    edif_flag = request.POST.get("edif_flag", None)
    if lat and lon and clientenro and precision:
        cli = Cliente.objects.get(clientenro=clientenro)
        cli.latitud = lat
        cli.longitud = lon
        cli.precision = precision
        cli.save()
        if edif_flag == "true":
            clientes = Cliente.objects.filter(
                direccion=cli.direccion)
            for c in clientes:
                c.latitud = lat
                c.longitud = lon
                c.precision = precision
                c.save()
        return HttpResponse(status=200)


def clientestable(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    global_search = request.GET['search[value]']
    if global_search:
        all_objects = Cliente.objects.filter(Q(latitud__isnull=True) &
                                             Q(direccion__icontains=global_search)
                                             | Q(clientenro__icontains=global_search)
                                             | Q(nombre__icontains=global_search)
                                             )
    else:
        all_objects = Cliente.objects.filter(latitud__isnull=True)
    columns = ['clientenro', 'nombre', 'direccion', 'posicion', 'edificio']
    objects = []

    for i in all_objects.order_by('clientenro')[start:start + length].values():
        clientenro = str(i["clientenro"])
        html_pos = "<button type=""button"" id=""{0}"" value=""{0}"" class=""{1}"">Obtener Posición</button>".format(
            clientenro, " btn")
        html_edif = "<div id=""edif"" class=""form-check""><label class=""form-check-label""><input class=""form-check-input"" type=""checkbox"" value=""{0}"">Es edificio?</label></div>".format(
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
    page = request.GET.get('page')
    paginator = Paginator(clientes, 10)
    try:
        clientes_pags = paginator.page(page)
    except PageNotAnInteger:
        clientes_pags = paginator.page(1)
    except EmptyPage:
        clientes_pags = paginator.page(paginator.num_pages)

    return render(request, 'web/completados.html', {"clientes": clientes_pags})


def table_completados(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    global_search = request.GET['search[value]']
    if global_search:
        all_objects = Cliente.objects.filter(Q(latitud__isnull=False) &
                                             Q(direccion__icontains=global_search)
                                             | Q(clientenro__icontains=global_search)
                                             | Q(nombre__icontains=global_search)
                                             )
    else:
        all_objects = Cliente.objects.filter(latitud__isnull=False)
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
