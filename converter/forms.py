from django import forms


class Download(forms.Form):
    link = forms.CharField(label='link')
