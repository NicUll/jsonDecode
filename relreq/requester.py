from os.path import join

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import requests


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

    def getmember(self, id):
        if self.checkurl(self.url):
            memberurl = join(self.url, 'customers/', id)
            print(memberurl)
            r = requests.get(memberurl, auth=(self.user, self.pwd))
            return r
        else:
            return "No valid url is set"
