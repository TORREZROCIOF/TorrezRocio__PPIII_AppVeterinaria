# core/forms.py
from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'mascota',
            'veterinario',
            'fecha_hora',
            'motivo',
            'estado',
            'observaciones',
            'duracion_minutos'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
