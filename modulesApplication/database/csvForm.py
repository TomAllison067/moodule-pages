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
    csv_upload.widget.attrs.update({'style': 'color:black', 'class':'csv_upload', 'required': 'required'})
    data.widget.attrs.update({'style': 'color:black', 'class':'', 'required': 'required'})

    def process_data(self, file, model):

        model_class = models[model]
        headers = (csv_converter.get_headers(model_class))
        # Wrapping the csv file uploaded to make it easier to read from
        f = io.TextIOWrapper(file)
        reader = csv.DictReader(f, delimiter=',', quotechar='"')

        result = []
        # used the csv readers created previously
        for row in reader:
            # checking if the csv file matches the type of model selected
            if headers != reader.fieldnames:
                return False
            attributes = row
            for key, value in attributes.items():
                if value.isnumeric():
                    attributes[key] = int(value)
                if value == 'FALSE':
                    attributes[key] = 0
                if value == 'TRUE':
                    attributes[key] = 1
            tmp = model_class(*attributes.values())
            tmp.clean()
            # If a new record is added to the csv file uploaded then the object is created
            if not model_class.objects.filter(pk=tmp.pk).exists():
                tmp.save()
            result.append(tmp)

        # using bulk_update to efficiently update the database, while not update the private key
        headers.remove(model_class._meta.pk.name)
        for field in headers:
            model_class.objects.bulk_update(result, [field])
        return model_class.__name__
