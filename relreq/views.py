import simplejson as simplejson
from django.core.serializers import json
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
                requester = Requester(request)
                requester.setup_request()
                # connection = request.POST.get("connection")
                # connectionString = Connection.objects.all().values_list('hosturl', flat=True).get(pk=connection)
                # gettype = request.POST.get("gettype")
                # gettypeString = GetType.objects.all().values_list('resourcepath', flat=True).get(pk=gettype)
                # querydata = request.POST.get("querydata")
                # requestText = connectionString + "/" + gettypeString + "/" + querydata
                # print(requestText)
                r = requester.make_request()
                data = requester.get_results_pretty()



            except Exception as e:
                print(e)
    return render(request, 'relreq/index.html', {'form': form, 'data': data})
