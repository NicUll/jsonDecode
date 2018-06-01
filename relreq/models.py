import json
from os.path import join

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class JSONCleaner(object):

    def __init__(self, parent):
        self.parent = parent
        self.new_groups = []
        self.new_entries = []

    def clean(self, json_text):
        data = json.loads(json_text)
        return_string = self.iter_dict(data, self.parent)
        return return_string

    def iter_dict(self, data, parent):
        return_string = "<section class='" + parent.name + "'>\n"

        if isinstance(data, list):
            for entry in data:
                return_string += self.iter_dict(entry, parent)
            return return_string

        for key, value in data.items():
            haschildren = isinstance(value, dict) or isinstance(value, list)
            jsonobj, created = JsonDictionaryEntry.objects.get_or_create(parent=parent, jsonvalue=key,
                                                                         defaults={
                                                                             'parent': parent,
                                                                             'displayvalue': key,
                                                                             'haschildren': haschildren})
            # if created:
            #     self.new_entries.append(key)
            if haschildren:
                dictgroupobj, created = DictGroup.objects.get_or_create(dictentryid=jsonobj.pk,
                                                                        defaults={'name': key, 'parent': parent.pk})
                # if created:
                #     self.new_groups.append(key)
                return_string += "<div class='group " + dictgroupobj.name + "'><p class='parent-name'>" + key + "</p>"
                return_string += self.iter_dict(value, dictgroupobj)
                return_string += "</div>"
            else:
                return_string += "<p class='entry'> %s: %s </p>" % (jsonobj.displayvalue, value)
        return_string += "\n</section>\n"
        return return_string


class Requester(object):
    validate = URLValidator()

    def __init__(self, request):
        self.request = request
        self.connection_url = ""
        self.login = None
        self.results = None
        self.jsoncleaner = None
        self.primary_dict_group = None

    def generate_connection_string(self):
        connection = self.request.POST.get("connection")
        return Connection.objects.all().values_list('hosturl', flat=True).get(pk=connection)

    def generate_get_type(self):
        gettype = self.request.POST.get("gettype")
        primary_dg_name = GetType.objects.all().values_list('resourcename', flat=True).get(pk=gettype) + "_prim_group"
        self.primary_dict_group, created = DictGroup.objects.get_or_create(name=primary_dg_name)
        return GetType.objects.all().values_list('resourcepath', flat=True).get(pk=gettype)

    def generate_querydata(self):
        return self.request.POST.get("querydata")

    def generate_connection_url(self, *args):
        self.connection_url = ""
        for arg in args:
            arg.strip("/")
            self.connection_url += arg + "/"
        if self.request.POST.get("getall"):
            self.connection_url += "info/"

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
        self.jsoncleaner = JSONCleaner(self.primary_dict_group)
        return self.jsoncleaner.clean(self.get_results_text())

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
    parent = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def delete_group(self, keep_sub=True):
        dict_entry_list = JsonDictionaryEntry.objects.filter(parent=self.pk)
        for entry in dict_entry_list:
            if not keep_sub:
                if entry.haschildren:
                    DictGroup.objects.get(dictentryid=entry.pk).delete_group(False)
                entry.delete()
            else:
                parent_entry, created = DictGroup.objects.get_or_create(pk=self.parent, defaults={"name": "virtual"})
                parent_entry_id = parent_entry.pk
                if created:
                    self.parent = parent_entry_id
                entry.parent = parent_entry_id

        self.delete()


class JsonDictionaryEntry(models.Model):
    parent = models.ForeignKey(DictGroup, on_delete=models.CASCADE)  # All should have parent, top level has main
    jsonvalue = models.CharField(max_length=20)
    displayvalue = models.CharField(max_length=40)
    haschildren = models.BooleanField()  # If it does, add to dictgroups
    #type = models.CharField(max_length=20)
    #attributes = models.CharField(max_length=300)

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
