from django.http import HttpResponseRedirect
from django.shortcuts import render

from relreq.models import Requester
from relreq.forms import RequestForm
import re


def index(request, data=None):
    form = RequestForm()
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid:
            return HttpResponseRedirect(reversed())

    return render(request, 'relreq/index.html', {'form': form})
