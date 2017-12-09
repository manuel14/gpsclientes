from openpyxl import load_workbook
from .models import Cliente


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
        if ws['E%s' % (r)].value is None:
            ws['E%s' % (r)].value = ""
        clientes.append(
            Cliente(
                clientenro=ws['A%s' % (r)].value,
                nombre=ws['B%s' % (r)].value + ws['C%s' % (r)].value,
                direccion=ws['D%s' % (r)].value + ws['E%s' % (r)].value
            )
        )
    Cliente.objects.bulk_create(clientes)
