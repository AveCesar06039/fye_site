# meetings/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Tenida, Asistencia

class TenidaForm(forms.ModelForm):
    class Meta:
        model = Tenida
        fields = ['fecha', 'tipo', 'grado', 'rls', 'tema', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'grado': forms.Select(attrs={'class': 'form-select'}),
            'rls': forms.Select(attrs={'class': 'form-select'}),
            'tema': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# --- LA MAGIA: Formset para la tabla de asistencia ---
AsistenciaFormSet = inlineformset_factory(
    Tenida, 
    Asistencia,
    fields=('miembro', 'puesto', 'presente', 'observaciones'),
    extra=0,          # No queremos filas vacías extra (ya las creó la señal)
    can_delete=False, # No borrar registros, solo marcar presente/ausente
    widgets={
        'puesto': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'observaciones': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
    }
)