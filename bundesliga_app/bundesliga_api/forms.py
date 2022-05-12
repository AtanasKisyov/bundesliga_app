from django import forms


class SearchForm(forms.Form):

    team = forms.CharField(
        max_length=250,
    )
