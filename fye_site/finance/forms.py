# B:\desarrollo\FeyEsp2.0\fye_site\finance\forms.py
from django import forms
from .models import Pago

class DateInput(forms.DateInput):
    input_type = "date"

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["rls", "miembro", "concepto", "monto", "estado", "fecha", "notas"]
        widgets = {"fecha": DateInput()}
