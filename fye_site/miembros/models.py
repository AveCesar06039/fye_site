# miembros/models.py
from django.db import models
from django.conf import settings

from rls.models import RLS


class Cargo(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Member(models.Model):
    GRADO_CHOICES = [
        ("AP", "Aprendiz"),
        ("CP", "Compañero"),
        ("MM", "Maestro"),
        ("PM", "Pass Master"),
    ]

    ESTADO_CHOICES = [
        ("ACT", "Activo"),
        ("SUE", "En sueños"),
        ("RET", "Retirado"),
    ]
    EMERGENCIA_RELACION_CHOICES = [
        ("CONYUJE", "Cónyuge"),
        ("HIJO", "Hijo/a"),
        ("PADRE", "Padre"),
        ("MADRE", "Madre"),
        ("HERMANO", "Hermano/a"),
        ("OTRO", "Otro"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="miembro",
    )

    rls = models.ForeignKey(
        RLS,
        on_delete=models.PROTECT,
        related_name="miembros",
    )

    # Número de registro autogenerado (string con ceros a la izquierda)
    numero_registro = models.CharField(
        max_length=5,
        unique=True,
        blank=True,
        null=True,
        help_text="Se asignará automáticamente.",
    )

    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True)

    foto = models.ImageField(
        upload_to="miembros/fotos/",
        blank=True,
        null=True,
    )

    fecha_nacimiento = models.DateField(
        "Fecha de nacimiento",
        blank=True,
        null=True,
    )
    fecha_iniciacion = models.DateField(
        "Fecha de iniciación",
        blank=True,
        null=True,
    )

    grado = models.CharField(
        max_length=3,
        choices=GRADO_CHOICES,
        default="AP",
    )

    estado = models.CharField(
        max_length=3,
        choices=ESTADO_CHOICES,
        default="ACT",
    )

    telefono_fijo = models.CharField(max_length=20, blank=True)
    numero_celular = models.CharField(max_length=20, blank=True)

    correo_electronico = models.EmailField(
        "Correo electrónico",
        max_length=254,
        blank=True,
        null=True,
    )

    correo_alterno = models.EmailField(
        "Correo alterno",
        max_length=254,
        blank=True,
        null=True,
    )

    domicilio_particular = models.TextField(blank=True)
    domicilio_trabajo = models.TextField(blank=True)

    # 🔴 NUEVOS CAMPOS DEL MIEMBRO
    
    tipo_sanguineo = models.CharField(
        "Tipo sanguíneo",
        max_length=3,
        blank=True,
        help_text="Ejemplo: O+, A-, B+",
    )

    emergencia_nombre = models.CharField(
        "Nombre contacto de emergencia",
        max_length=150,
        blank=True,
    )
    emergencia_relacion = models.CharField(
        max_length=10,
        choices=EMERGENCIA_RELACION_CHOICES,
        default="OTRO"
    )
    emergencia_telefono = models.CharField(
        "Teléfono contacto de emergencia",
        max_length=20,
        blank=True,
    )
    emergencia_telefono_alterno = models.CharField(
        "Teléfono alterno contacto de emergencia",
        max_length=20,
        blank=True,
    )
    emergencia_domicilio = models.TextField(
        "Domicilio contacto de emergencia",
        blank=True,
    )

    observaciones = models.TextField(
        "Observaciones (alergias, datos importantes)",
        blank=True,
    )

    cargo_actual = models.ForeignKey(
        Cargo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="miembros_actuales",
    )

    creado = models.DateTimeField(
        "Creado",
        auto_now_add=True,
        null=True,
        blank=True,
    )
    modificado = models.DateTimeField("Modificado", auto_now=True)

    class Meta:
        ordering = ["rls__nombre", "primer_apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.primer_apellido} ({self.numero_registro or 's/n'})"

    def save(self, *args, **kwargs):
        """
        Asigna numero_registro automáticamente si viene vacío.
        Usa el id autoincremental como base y lo formatea con ceros a la izquierda.
        """
        if not self.numero_registro:
            ultimo = Member.objects.order_by("-id").first()
            if ultimo and ultimo.numero_registro and ultimo.numero_registro.isdigit():
                siguiente = int(ultimo.numero_registro) + 1
            else:
                siguiente = (ultimo.id + 1) if ultimo else 1
            # max_length=5 → 5 dígitos
            self.numero_registro = str(siguiente).zfill(5)
        super().save(*args, **kwargs)


class Beneficiario(models.Model):
    RELACION_CHOICES = [
        ("CONYUJE", "Cónyuge"),
        ("HIJO", "Hijo/a"),
        ("PADRE", "Padre"),
        ("MADRE", "Madre"),
        ("HERMANO", "Hermano/a"),
        ("OTRO", "Otro"),
    ]

    # Usa la FK real que tiene datos: miembro_id
    member = models.ForeignKey(
        "Member",
        on_delete=models.CASCADE,
        related_name="beneficiarios",
        db_column="miembro_id",   # 👈 apuntas a la columna correcta
    )

    nombre = models.CharField(max_length=120)
    primer_apellido = models.CharField(max_length=120)
    segundo_apellido = models.CharField(max_length=120)

    fecha_nacimiento = models.DateField(null=True, blank=True)
    domicilio = models.TextField()
    telefono = models.CharField(max_length=30)
    relacion = models.CharField(
        max_length=20,
        choices=RELACION_CHOICES,
        blank=True,
        null=True,
    )
    
    porcentaje = models.IntegerField(null=True, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "miembros_beneficiario"

    @property
    def nombre_completo(self):
        # Para que tus templates sigan usando nombre_completo sin romper
        return f"{self.nombre} {self.primer_apellido} {self.segundo_apellido}".strip()
    def __str__(self):
        relacion = self.get_relacion_display() if self.relacion else ""
        return f"{self.nombre_completo} ({relacion})" if relacion else self.nombre_completo
    def __str__(self):
        return self.nombre_completo


class CargoHistorico(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="historial_cargos",
    )
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Historial de cargo"
        verbose_name_plural = "Historial de cargos"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.member} - {self.cargo} ({self.fecha_inicio} - {self.fecha_fin or 'Actual'})"