import csv

from django.http import HttpResponse
from django.utils import timezone

from modulesApplication.models import ModuleSelection


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


def csv_student_selections():
    queryset = ModuleSelection.objects.all()
    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields] + ['module_codes']

    response = HttpResponse(content_type='text.csv')
    filename = f'moduleSelections-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
    response['Content-Disposition'] = f'attachment; filename={filename}'

    writer = csv.writer(response)
    writer.writerow(field_names)
    for i in range(len(queryset)):
        mod_codes = [m.mod_code for m in queryset[i].module_set.all()]
        writer.writerow(
            list(queryset.values_list()[i]) + [mod_codes])
    return response
