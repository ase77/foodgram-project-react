import csv
import io

from django.http import FileResponse, HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def download_csv(ingredients):
    value_dict = {}
    for item in ingredients:
        name = item[0]
        if name not in value_dict:
            value_dict[name] = {
                'ед.изм.': item[1],
                'кол-во': item[2]
            }
        else:
            value_dict[name]['кол-во'] += item[2]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_cart.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'amount', 'measurement_unit'])
    for key, value in value_dict.items():
        writer.writerow([key, value["кол-во"], value["ед.изм."]])
    return response


def download_txt(ingredients):
    value_dict = {}
    for item in ingredients:
        name = item[0]
        if name not in value_dict:
            value_dict[name] = {
                'ед.изм.': item[1],
                'кол-во': item[2]
            }
        else:
            value_dict[name]['кол-во'] += item[2]
    value_list = ''
    value_list += 'ингредиент (ед.изм.) - кол-во\n'
    for key, value in value_dict.items():
        value_list += f'{key} ({value["ед.изм."]}) - {value["кол-во"]}\n'
    return HttpResponse(value_list, content_type='text/plain')


def download_pdf(ingredients):
    value_dict = {}
    for item in ingredients:
        name = item[0]
        if name not in value_dict:
            value_dict[name] = {
                'ед.изм.': item[1],
                'кол-во': item[2]
            }
        else:
            value_dict[name]['кол-во'] += item[2]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    p.setFont("Verdana", 10)
    x = 30
    y = 780
    p.drawString(x, y + 20, ('ингредиент (ед.изм.) - кол-во'))
    for key, value in value_dict.items():
        p.drawString(
            x, y, (f'{key} ({value["ед.изм."]}) - {value["кол-во"]}')
        )
        y -= 15
    p.showPage()
    p.save()
    return response
