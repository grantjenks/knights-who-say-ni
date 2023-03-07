from django import forms


class UserForm(forms.Form):
    user = forms.CharField(max_length=200)
