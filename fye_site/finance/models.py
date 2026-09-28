# B:\desarrollo\FeyEsp2.0\fye_site\finance\models.py
from django.db import models

class Pago(models.Model):
    ESTADOS = [("PEN","Pendiente"), ("PAG","Pagado"), ("CAN","Cancelado")]
    rls = models.ForeignKey("rls.RLS", on_delete=models.PROTECT, related_name="pagos")
    miembro = models.ForeignKey("miembros.Member", on_delete=models.PROTECT, related_name="pagos")
    concepto = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=3, choices=ESTADOS, default="PEN")
    fecha = models.DateField()
    notas = models.TextField(blank=True)  # <- NUEVO

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha", "-id"]
