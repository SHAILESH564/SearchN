
from django import forms
from .models import SearchN

class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchN
        # fields = ['query']
        fields = '__all__'
