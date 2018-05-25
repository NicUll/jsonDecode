from django.shortcuts import render

from relreq.models import Requester
import re


def index(request):
    requester = Requester();
    requester.setlogin()
    requester.seturl()
    r = requester.getmember()
    r = re.sub('{|}|"', "", r)
    info_list = r.split(",")
    context = {'request_result': info_list}
    return render(request, 'relreq/index.html', context)
