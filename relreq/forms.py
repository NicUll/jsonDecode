from django import forms

from relreq.models import Connection, GetType


class RequestForm(forms.Form):
    connection = forms.ModelChoiceField(queryset=Connection.objects.all().order_by('hostname'), initial=0)
    connection.widget.attrs['id'] = 'connection'
    gettype = forms.ModelChoiceField(queryset=GetType.objects.all().order_by('resourcename'), initial=0, label="Get Type")
    gettype.widget.attrs['class'] = 'line-flex'
    getall = forms.BooleanField(initial=True, label="Get All", required=False)
    getall.widget.attrs['class'] = 'line-flex'
    querydata = forms.CharField(max_length=50, required=False)
    querydata.widget.attrs['placeholder'] = 'Query Data'


