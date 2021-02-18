from django.shortcuts import render

from ..programmeInfo import csv_converter
from ..models import Module, Programme, ModuleSelection


def landing(request):
    return render(request, 'officePages/OfficeLanding.html')


def csv_file(request):

    return csv_converter.model_to_csv(Programme)
