from django import forms
from .models import Reservation
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room','start_at','end_at','note']
        widgets = {'start_at': forms.DateTimeInput(attrs={'type':'datetime-local'}),
                   'end_at': forms.DateTimeInput(attrs={'type':'datetime-local'})}
