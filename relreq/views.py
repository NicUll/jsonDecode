from django.http import HttpResponseRedirect
from django.shortcuts import render

from relreq.models import Requester
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
                gettype = request.POST.get("gettype")
                querydata = request.POST.get("querydata")

                r = requests.get(connection.generateurl())


    return render(request, 'relreq/index.html', {'form': form, 'data': data})
