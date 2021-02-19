import csv

from django import forms
import io
from ..models import Programme, Module, ModuleSelection, People
from modulesApplication.database.csv_reader import CsvReader

# MODEL_CHOICES =(
#     ("Programme", Programme),
#     ("Module", Module),
#     ("Module Selection", ModuleSelection),
# )
MODEL_CHOICES = (
    (1, "Programme"),
    (2, "Module"),
    (3, "Module Selection"),
    (4, "People")
)
models = {'1': Programme, '2': Module, '3': ModuleSelection, '4':People}


class CsvUploadForm(forms.Form):
    data_file = forms.FileField()
    model = forms.ChoiceField(choices=MODEL_CHOICES)

    # model = forms.Select(choices=('Programme', ModuleSelection))

    def process_data(self, file, model):

        model_class = models[model]
        model_class.objects.all().delete()
        result = []
        f = io.TextIOWrapper(file)
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            attributes = row
            for key, value in attributes.items():
                if value.isnumeric():
                    attributes[key] = int(value)
            tmp = model_class(*attributes.values())
            result.append(tmp)
        model_class.objects.bulk_create(result)
