import csv

from modulesApplication.database.models import Module


class CsvReader:
    """
    A CsvReader to read in data from a csv file.
    The CsvReader can read headers from a csv file, as well as rows, and return a list of Model objects according
    to the type that was read in.
    The models dict maps the type of data read in to the type of Model object it is represented by. For example,
    the key "MODULE" maps to the Module class.
    """
    # Maps strings to objects from models.py
    models = {"MODULE": Module}

    def read_headers(self, filename):
        """
        Reads the headers of the csv file.
        :param filename: the path of the file to read.
        :return: the headers from the csv file.
        """
        with open(file=filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                return row

    def read_table(self, filename, model: str):
        """
        Read a csv file corresponding to one database table, and return a list of appropriate Model objects
        according to that file. For example, setting model to "MODEL" will assume the csv corresponds to rows
        of attributes that are the same as the Model class's attributes.
        :param filename: the path of the csv file to read.
        :param model: the type of Model to attempt to read and instantiate.
        :return: A list of Model objects.
        """
        which_class = self.models.get(model.upper())
        result = []
        with open(file=filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                attributes = row
                for key, value in attributes.items():
                    if value.isnumeric():
                        attributes[key] = int(value)
                tmp = which_class(*attributes.values())
                result.append(tmp)
        return result
