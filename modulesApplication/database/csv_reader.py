import csv

from django.db.models.base import ModelBase

from modulesApplication.database.models.programme import Programme
from modulesApplication.database.models.strand import Strands


class CsvReader:
    """
    A CsvReader to read in data from a csv file.
    The CsvReader can read headers from a csv file, as well as rows, and return a list of Model objects according
    to the type that was read in.
    """

    def read_headers(self, filename):
        """
        Reads the headers of the csv file.
        :param filename: the path of the file to read.
        :return: the headers from the csv file.
        """
        with open(file=filename, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                return row

    def read_table(self, filepath, model_class: ModelBase):
        """
        Read ALL HEADERS from a csv file corresponding to one database table into a list of Model objects.
        :param filepath: the path of the csv file to read.
        :param model_class: the type of Model to read in
        :return: A list of Model objects.
        """
        result = []
        with open(file=filepath, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                attributes = row
                for key, value in attributes.items():
                    if value.isnumeric():
                        attributes[key] = int(value)
                tmp = model_class(*attributes.values())
                result.append(tmp)
        return result

    def read_table_partial(self, filepath, model_class):
        """
        Read from a csv file into a model, reading only those headers which the model has as a field and no more.
        :param filepath: the path of the csv file
        :param model_class: the target model class
        :return: a list of model objects
        """
        result = []
        with open(file=filepath, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                attributes = row
                args = {}
                for key, value in attributes.items():
                    if value.isnumeric():
                        attributes[key] = int(value)
                    if hasattr(model_class, key):
                        args[key] = value
                tmp = model_class(*args.values())
                result.append(tmp)
        return result
