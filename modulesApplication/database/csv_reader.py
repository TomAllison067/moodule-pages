import csv

from django.db.models.base import ModelBase


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
        Read a csv file corresponding to one database table, and return a list of appropriate Model objects
        according to that file.
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
