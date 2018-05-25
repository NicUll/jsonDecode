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
