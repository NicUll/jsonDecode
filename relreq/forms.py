from django import forms


class RequestForm(forms.Form):

    environment = forms.CharField(label='Miljö', max_length=100)
    id = forms.CharField(label='Id', max_length=40)