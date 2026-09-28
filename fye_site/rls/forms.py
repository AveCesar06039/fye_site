# rls/forms.py
from django import forms
from .models import RLS

class RLSForm(forms.ModelForm):
    class Meta:
        model = RLS
        fields = ["nombre", "numero", "homenaje_a", "dia_trabajo", "hora_trabajo", "lugar"]
        widgets = {
            "hora_trabajo": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }
