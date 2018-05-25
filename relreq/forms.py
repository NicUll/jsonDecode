from django import forms

from relreq.models import Connection


class RequestForm(forms.Form):
    connection = forms.ModelChoiceField(queryset=Connection.objects.all().order_by('hostname'), initial=0)
    #gettype = forms.ModelChoiceField(queryset=GetType.objects.all().order_by('resourcename'), initial=0)
    querydata = forms.CharField(max_length=50)
