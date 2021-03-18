import csv

from django import forms
import io
from ..models import Programme, Module, ModuleSelection, People
from ..programmeInfo import csv_converter

MODEL_CHOICES = (
    (1, "Programme"),
    (2, "Module"),
    (3, "Module Selection")
)
models = {'1': Programme, '2': Module, '3': ModuleSelection, '4': People}


class CsvUploadForm(forms.Form):
    csv_upload = forms.FileField()
    data = forms.ChoiceField(choices=MODEL_CHOICES)
    data.widget.attrs.update({'style': 'color:black', 'class':'', 'required': 'required'})

    def process_data(self, file, model):

        model_class = models[model]
        headers = (csv_converter.get_headers(model_class))
        result = []
        f = io.TextIOWrapper(file)
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            if headers != reader.fieldnames:
                return False
            attributes = row

            try:
                for key, value in attributes.items():

                    print(key)
                    print(value)
                    if value.isnumeric():
                        attributes[key] = int(value)
                    if value == 'FALSE':
                        attributes[key] = 0
                    if value == 'TRUE':
                        attributes[key] = 1
            except IndexError:
                continue

            tmp = model_class(*attributes.values())
            tmp.clean()
            if not model_class.objects.filter(pk=tmp.pk).exists():
                tmp.save()
            result.append(tmp)

        headers.remove(model_class._meta.pk.name)
        for field in headers:
            model_class.objects.bulk_update(result, [field])
        return model_class.__name__
