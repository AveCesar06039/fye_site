# B:\desarrollo\FeyEsp2.0\fye_site\meetings\models.py
from django.conf import settings
from django.db import models
# Si tienes un modelo de 'RLS' en otra app, asegúrate de importarlo o usar string reference como hiciste.
# --- 1. AGREGA ESTOS IMPORTS AL INICIO DEL ARCHIVO ---
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
class Tenida(models.Model):
    # ... (Tus opciones de TIPO y GRADO se quedan igual) ...
    TIPO_CHOICES = [
        ("ORD", "Ordinaria"),
        ("EXT", "Extraordinaria"),
        ("INST", "Instalación"),
        ("ESP", "Especial"),
        ("FUN", "Fúnebre"),
        ("BLA", "Tenida Blanca"),
    ]

    GRADO_CHOICES = [
        ("APR", "Aprendiz"),
        ("COM", "Compañero"),
        ("MAE", "Maestro"),
    ]

    rls = models.ForeignKey(
        "rls.RLS",
        on_delete=models.PROTECT,
        related_name="tenidas",
        verbose_name="R.L.S."
    )
    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="ORD")
    grado = models.CharField(max_length=3, choices=GRADO_CHOICES, default="APR")
    tema = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Tenida"
        verbose_name_plural = "Tenidas"

    def __str__(self):
        return f"{self.fecha} - {self.tipo} ({self.get_grado_display()})"


class Asistencia(models.Model):
    # --- AGREGAMOS LAS OPCIONES DE CARGOS DEL DÍA ---
    # Estos son los puestos que ocuparon SOLO POR ESE DÍA
    CARGOS_CHOICES = [
        ('VM', 'Venerable Maestro'),
        ('PV', 'Primer Vigilante'),
        ('SV', 'Segundo Vigilante'),
        ('OR', 'Orador'),
        ('SE', 'Secretario'),
        ('TE', 'Tesorero'),
        ('MC', 'Maestro de Ceremonias'),
        ('EX', 'Experto'),
        ('GT', 'Guarda Templo'),
        ('HI', 'Hospitalario'),
        ('JD', 'Sin Cargo (Columna)'), # Opción por defecto
        ('VI', 'Visitante'),
    ]

    tenida = models.ForeignKey(Tenida, on_delete=models.CASCADE, related_name="asistencias")
    
    miembro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="asistencias",
        verbose_name="Hermano"
    )

    # --- NUEVO CAMPO SOLICITADO ---
    puesto = models.CharField(
        max_length=3, 
        choices=CARGOS_CHOICES, 
        default='JD',
        verbose_name="Puesto del Día"
    )

    presente = models.BooleanField(default=True, verbose_name="¿Asistió?")
    observaciones = models.CharField(max_length=255, blank=True, help_text="Ej: Llegó tarde, se retiró temprano")

    class Meta:
        unique_together = [("tenida", "miembro")]
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"
        ordering = ['miembro'] 

    def __str__(self):
        return f"{self.miembro} - {self.get_puesto_display()}"
    
    # --- 2. AGREGA ESTO AL FINAL DEL ARCHIVO (FUERA DE LAS CLASES) ---

@receiver(post_save, sender=Tenida)
def generar_lista_asistencia_automatica(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente cada vez que se guarda una Tenida.
    Si es una Tenida NUEVA (created=True), busca a todos los usuarios activos
    y les crea un registro de asistencia vacío.
    """
    if created:
        User = get_user_model()
        
        # 1. Filtramos a los Hermanos Activos
        # Ajusta el filtro si usas otro campo para definir quién es miembro activo
        hermanos_activos = User.objects.filter(is_active=True)
        
        lista_asistencia = []
        
        for hermano in hermanos_activos:
            lista_asistencia.append(
                Asistencia(
                    tenida=instance,
                    miembro=hermano,
                    puesto='JD',      # Puesto por defecto (ej: Sin Cargo/Juan de la Calle)
                    presente=False,   # Por defecto NO presente (para que pases lista)
                    observaciones=""
                )
            )
        
        # 2. Guardamos todos de golpe (Más eficiente que guardar uno por uno)
        if lista_asistencia:
            Asistencia.objects.bulk_create(lista_asistencia)