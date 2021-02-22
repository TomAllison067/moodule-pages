import csv

from django.utils import timezone
from django.http import HttpResponse


def get_headers(model_class):
    model = model_class.objects.model
    model_fields = model._meta.fields + model._meta.many_to_many
    headers = [field.name for field in model_fields]
    return headers


def model_to_csv(model_class):
    # creating a unique filename for the csv
    filename = f'{model_class.__name__}-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
    response = HttpResponse(content_type='text/csv')

    # initialising the csv writer
    writer = csv.writer(response)
    # get the headers to write to the top of the csv file
    headers = get_headers(model_class)
    writer.writerow(headers)

    # getting all the objects from the database and writing each line to the csv
    for member in model_class.objects.all().values_list(*headers):
        writer.writerow(member)
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response
