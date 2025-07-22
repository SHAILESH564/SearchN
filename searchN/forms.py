
from django import forms
from .models import Reservation, SearchN

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'

class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchN
        # fields = ['query']
        fields = '__all__'
