from openpyxl import load_workbook
from .models import Cliente, Calle


def load_clientes():

    wb = load_workbook('clientes_sin_localizar.xlsx')
    ws = wb.get_sheet_by_name('clientes')
    clientes = []
    for r in range(2, ws.max_row + 1):
        if ws['B%s' % (r)].value is None:
            ws['B%s' % (r)].value = ""
        if ws['C%s' % (r)].value is None:
            ws['C%s' % (r)].value = ""
        if ws['D%s' % (r)].value is None:
            ws['D%s' % (r)].value = ""
        if ws['E%s' % (r)].value is None and ws['G%s' % (r)].value is None:
            continue
        if ws['E%s' % (r)].value is None:
            ws['E%s' % (r)].value = ""
        if ws['G%s' % (r)].value is None:
            ws['G%s' % (r)].value = ""
        if ws['H%s' % (r)].value is None:
            ws['H%s' % (r)].value = ""
        if ws['I%s' % (r)].value is None:
            ws['I%s' % (r)].value = ""
        if ws['J%s' % (r)].value == "NO":
            geocode = False
        else:
            geocode = True
        clientes.append(
            Cliente(
                clientenro=ws['A%s' % (r)].value,
                nombre=ws['B%s' % (r)].value + " " + ws['C%s' % (r)].value,
                direccion=ws['D%s' % (r)].value + " " +
                str(ws['E%s' % (r)].value),
                tira=ws['G%s' % (r)].value,
                piso=ws['H%s' % (r)].value,
                depto=ws['I%s' % (r)].value,
                geocode=geocode
            )
        )
    Cliente.objects.bulk_create(clientes)


def load_calles():
    wb = load_workbook('calles_completo.xlsx')
    ws = wb.get_sheet_by_name('calles_completo')
    calles = []
    for r in range(2, ws.max_row + 1):
        if ws['F%s' % (r)].value is None or ws['F%s' % (r)].value == "":
            continue
        if ws['B%s' % (r)].value is None or ws['A%s' % (r)].value == "":
            lim_inf = None
        else:
            lim_inf = ws['B%s' % (r)].value
        if ws['C%s' % (r)].value is None or ws['C%s' % (r)].value == "":
            lim_sup = None
        else:
            lim_sup = ws['C%s' % (r)].value
        if ws['D%s' % (r)].value == 'SI':
            geocode = True
        else:
            geocode = False
        if ws['E%s' % (r)].value == 'SI':
            osm_geocode = True
        elif ws['E%s' % (r)].value == 'NO':
            osm_geocode = False
        else:
            osm_geocode = None
        c = Calle(
            nombre=ws['A%s' % (r)].value,
            limite_inferior=lim_inf,
            limite_superior=lim_sup,
            calleidsiga=ws['F%s' % (r)].value,
            geocode=geocode,
            osm_geocode=osm_geocode
        )
        calles.append(c)
    Calle.objects.bulk_create(calles)
    return True
