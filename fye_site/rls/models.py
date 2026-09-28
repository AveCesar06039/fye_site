from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

# rls/models.py
from django.db import models

class RLS(models.Model):
    DIAS = [
        ("LUN", "Lunes"),
        ("MAR", "Martes"),
        ("MIE", "Miércoles"),
        ("JUE", "Jueves"),
        ("VIE", "Viernes"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]

    nombre = models.CharField(max_length=200)
    numero = models.CharField(max_length=50, blank=True)
    homenaje_a = models.CharField(max_length=200, blank=True)
    dia_trabajo = models.CharField(max_length=3, choices=DIAS, blank=True)   # <- nuevo
    hora_trabajo = models.TimeField(null=True, blank=True)                   # <- nuevo
    lugar = models.CharField(max_length=250, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre", "numero"]

    def __str__(self):
        return f"{self.nombre} {self.numero}".strip()

