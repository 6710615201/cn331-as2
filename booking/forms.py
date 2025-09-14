from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room','start_at','end_at','note']
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }
    def clean(self):
        cleaned = super().clean()
        room = cleaned.get('room')
        start_at = cleaned.get('start_at')
        end_at = cleaned.get('end_at')
        if room and start_at and end_at:
            delta = end_at - start_at
            hours = delta.total_seconds() / 3600
            if hours <= 0:
                raise forms.ValidationError('ช่วงเวลาไม่ถูกต้อง')
            if hours > room.max_hours:
                raise forms.ValidationError(f'ห้องนี้จองได้สูงสุด {room.max_hours} ชั่วโมงต่อครั้ง')
        return cleaned
