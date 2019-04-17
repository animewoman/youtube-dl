from django import forms


class Download(forms.Form):
    link = forms.CharField(label='link', required=True)
    email = forms.EmailField(label='email', required=True)
