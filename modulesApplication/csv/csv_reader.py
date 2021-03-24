import csv
from typing import List

from django.db.models.base import ModelBase

from modulesApplication.database.option_rule import OptionRule
from modulesApplication.database.programme import Programme


class CsvReader:
    """
    A `CsvReader` can read .csv files and convert the data into appropriate data model classes for our database.

    We've tried to be generic, and the ``read_table_partial`` method is probably the most appropriate method
    for most cases.
    """

    def read_headers(self, filename) -> List[str]:
        """
        Reads the headers (the first row) of a .csv file and returns it.

        Args:
            filename: the file to read in.

        Returns:
            A List[str] of containing the headers in the first row of the .csv file.
        """
        with open(file=filename, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                return row

    def read_table(self, filepath, model_class: ModelBase):
        """
        DEPRECATED!

        Reads a .csv file corresponding to a data model, and builds a list of the corresponding model objects.

        Args:
            filepath: the file to read.
            model_class: the desired model class.

        Returns:
            A list of model objects.
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

        A more flexible, generic, better version of ``read_table`` that doesn't require your .csv file to have
        exactly the same number of headers as the target model class.

        For example, our application only has some fields in the `Programme` model compared to the example sqlite
        database. This method will only read in the appropriate headers. Use this one!

        Args:
            filepath: the file to read in.
            model_class: the target model to read in to.

        Returns:
            A list of appropriate model objects.
        """
        result = []
        with open(file=filepath, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                attributes = row
                kwargs = {}
                for key, value in attributes.items():
                    if value.isnumeric():
                        attributes[key] = int(value)
                    if hasattr(model_class, key):
                        kwargs[key] = value
                if model_class is OptionRule and kwargs['prog_code']:
                    # TODO less bad hack
                    # REALLY HACKY, BAD WAY to import foreign keys of OptionRule.
                    kwargs['prog_code'] = Programme.objects.get(prog_code=kwargs['prog_code'])
                tmp = model_class(**kwargs)
                result.append(tmp)
        return result

    def read_dict(self, file):
        """
        Reads a .csv file and converts it into a list of dictionaries.

        Args:
            file: the file to read

        Returns:
            A list of [header:value] dictionaries.
        """
        with open(file, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            return list(reader)