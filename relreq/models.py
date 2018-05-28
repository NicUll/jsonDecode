import json
from os.path import join

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class JSONCleaner(object):

    def __init__(self, dict_table):
        self.dict_table = dict_table
        self.json_list = []

    def clean(self, json_text):
        data = json.loads(json_text)
        print(data["accountNumber"])


class Requester(object):
    validate = URLValidator()

    def __init__(self, request):
        self.request = request
        self.connection_url = ""
        self.login = None
        self.results = None
        self.jsoncleaner = None

    def generate_connection_string(self):
        connection = self.request.POST.get("connection")
        return Connection.objects.all().values_list('hosturl', flat=True).get(pk=connection)

    def generate_get_type(self):
        gettype = self.request.POST.get("gettype")
        return GetType.objects.all().values_list('resourcepath', flat=True).get(pk=gettype)

    def generate_querydata(self):
        return self.request.POST.get("querydata")

    def generate_connection_url(self, *args):
        self.connection_url = ""
        for arg in args:
            arg.strip("/")
            self.connection_url += arg + "/"

    def generate_login(self):
        self.login = Connection.objects.get(pk=self.request.POST.get("connection")).getlogin()

    def setup_request(self):
        self.generate_connection_url(self.generate_connection_string(), self.generate_get_type(),
                                     self.generate_querydata())
        self.generate_login()

    def make_request(self):
        self.results = requests.get(self.connection_url, auth=self.login)

    def get_results_text(self):
        return self.results.text

    def get_results_pretty(self):
        self.jsoncleaner = JSONCleaner(JsonDictionaryEntry.objects.all())
        self.jsoncleaner.clean(self.get_results_text())

    # return values


class Settings(object):

    def __init__(self):
        self._data = {}

    def addsetting(self, name, value):
        if isinstance(name, str):
            self._data[name] = value
            return True
        return False

    def getsetting(self, name):
        if isinstance(name, str):
            return self._data.get(name)
        return None


class Connection(models.Model):
    validate = URLValidator()
    hostname = models.CharField(max_length=200)
    hosturl = models.CharField(max_length=200)
    restuser = models.CharField(max_length=20)
    restpass = models.CharField(max_length=20)

    def __str__(self):
        return self.hostname

    @staticmethod
    def checkurl(url):
        try:
            Connection.validate(url)
            return True
        except ValidationError as e:
            return False

    def save(self, *args, **kwargs):
        if "/api" not in self.hosturl:
            self.storefullurl(".abalonrelevate.se/api/v1")
        if self.checkurl(self.hosturl):
            super(*args, **kwargs).save()

    def getlogin(self):
        return self.restuser, self.restpass

    def generateurl(self, baseurl):
        return "https://" + self.hosturl + baseurl

    def storefullurl(self, baseurl):
        self.hosturl = self.generateurl(baseurl)


class DictGroup(models.Model):
    name = models.CharField(max_length=40)
    dictentryid = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class JsonDictionaryEntry(models.Model):
    parent = models.ForeignKey(DictGroup, on_delete=models.CASCADE)  # All should have parent, top level has main
    jsonvalue = models.CharField(max_length=20)
    displayvalue = models.CharField(max_length=40)
    haschildren = models.BooleanField()  # If it does, add to dictgroups

    def __str__(self):
        return self.displayvalue

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.haschildren and not DictGroup.objects.filter(dictentryid=self.pk).exists():
            dg = DictGroup(dictentryid=self.pk, name=self.displayvalue)
            dg.save()


class GetType(models.Model):
    resourcepath = models.CharField(max_length=30)
    resourcename = models.CharField(max_length=200)

    def __str__(self):
        return self.resourcename
