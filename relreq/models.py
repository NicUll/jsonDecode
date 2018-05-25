from os.path import join

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class Requester(object):
    validate = URLValidator()

    def __init__(self):
        self.url = ""
        self.user = ""
        self.pwd = ""

    def seturl(self, url):
        if self.checkurl(url):
            self.url = url

    @staticmethod
    def checkurl(url):
        try:
            Requester.validate(url)
            return True
        except ValidationError as e:
            return False

    def setlogin(self, user, pwd):
        self.user = user
        self.pwd = pwd
        print(self.user)
        print(self.pwd)

    def getmember(self, id):
        if self.checkurl(self.url):
            memberurl = join(self.url, 'customers/', id)
            print(memberurl)
            r = requests.get(memberurl, auth=(self.user, self.pwd))
            return r.text
        else:
            return "No valid url is set"


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
    hostname = models.CharField(max_length=200)
    hosturl = models.CharField(max_length=200)
    restuser = models.CharField(max_length=20)
    restpass = models.CharField(max_length=20)

    def __str__(self):
        return self.hostname

    def getlogin(self):
        return self.restuser, self.restpass

    def generateurl(self, baseurl):
        return str.join("https://", self.hosturl, baseurl)

    def storefullurl(self, baseurl):
        self.hosturl = self.generateurl()


class DictGroup(models.Model):
    name = models.CharField(max_length=40)
    dictentryid = models.IntegerField(null=True, blank=True)
    rules = models.CharField(max_length=20, null=True, blank=True)

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
        if self.haschildren:
            dg = DictGroup(dictentryid=self.pk)
            dg.save()


class GetType(models.Model):
    resourcepath = models.CharField(max_length=30)
    resourcename = models.CharField(max_length=200)

    def __str__(self):
        return self.resourcename
