from relreq.models import Connection, GetType, JsonDictionaryEntry
import requests

class DataRequest(object):

    def __init__(self, connection, gettype):
        self.connection = connection
        self.gettype = gettype
        self.dictionary = self.gettype.dictionary
        self.latestrequest = None

    def makerequest(self):
        r = requests.get(self.connection.hosturl, auth=(self.connection.getlogin()))
        if r.status_code == 200:
            self.latestrequest = r
            return True
        else:
            return False

    def getlatestrequest(self):
        return self.latestrequest


