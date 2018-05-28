

from django.http import HttpResponseRedirect
from django.shortcuts import render

from relreq.models import Requester, Connection, GetType
from relreq.forms import RequestForm
import re
import requests


def index(request):
    data = None
    form = RequestForm()
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid:
            try:
                connection = request.POST.get("connection")
                connectionString = Connection.objects.all().values_list('hosturl', flat=True).get(pk=connection)
                gettype = request.POST.get("gettype")
                gettypeString = GetType.objects.all().values_list('resourcepath', flat=True).get(pk=gettype)
                querydata = request.POST.get("querydata")
                requestText = connectionString + "/" + gettypeString + "/" + querydata
                r = requests.get(requestText, auth=(Connection.objects.all().get(connection).getlogin()))
                print(r.text)
            except Exception as e:
                print(e)

    return render(request, 'relreq/index.html', {'form': form, 'data': data})
