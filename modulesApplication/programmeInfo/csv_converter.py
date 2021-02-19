import csv

from django.utils import timezone
from django.http import HttpResponse


def get_headers(model_class):
    model = model_class.objects.model
    model_fields = model._meta.fields + model._meta.many_to_many
    headers = [field.name for field in model_fields]
    return headers


def model_to_csv(model_class):
    headers = get_headers(model_class)
    filename = f'{model_class.__name__}-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(headers)
    for member in model_class.objects.all().values_list(*headers):
        writer.writerow(member)
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response
