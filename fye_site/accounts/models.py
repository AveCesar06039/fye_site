# accounts/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

# ----------------------------------------
# USER == MIEMBRO
# ----------------------------------------
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _normalize_rls_in_extra(self, extra):
        # Si RLS llega como id (texto) en createsuperuser, conviértelo a rls_id
        if 'rls' in extra:
            rls_val = extra.pop('rls')
            if rls_val is None:
                extra['rls'] = None
            else:
                try:
                    extra['rls_id'] = int(rls_val)
                except (TypeError, ValueError):
                    # Si ya es instancia o no convertible, déjalo como viene
                    extra['rls'] = rls_val
        return extra

    def _ensure_numero_registro(self, extra):
        # Genera uno único si viene vacío (evita el "TEMP" duplicado)
        if not extra.get('numero_registro'):
            extra['numero_registro'] = f"USR-{get_random_string(8).upper()}"
        return extra

    def _create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        extra = self._normalize_rls_in_extra(extra)
        extra = self._ensure_numero_registro(extra)

        user = self.model(email=email, **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    # Usamos email como identificador
    username = None
    email = models.EmailField("Correo electrónico", unique=True)

    # Número de registro (UN SOLO campo, sin default "TEMP")
    numero_registro = models.CharField("Número de registro", max_length=50, unique=True)

    # Relación con RLS (UNA sola definición)
    rls = models.ForeignKey(
        "rls.RLS",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="usuarios",
        verbose_name="RLS",
    )

    # Identidad base
    first_name = models.CharField("Nombre", max_length=120)
    last_name = models.CharField("Primer apellido", max_length=120)
    second_surname = models.CharField("Segundo apellido", max_length=120, blank=True)

    # Datos masónicos
    GRADOS = [("APR","Aprendiz"), ("COM","Compañero"), ("MAE","Maestro")]
    ESTADO = [("ACT","Activo"), ("SUE","En sueños")]
    grado = models.CharField(max_length=3, choices=GRADOS, default="APR")
    fecha_iniciacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=ESTADO, default="ACT")

    # Contacto básico
    numero_celular = models.CharField("Celular", max_length=30, blank=True)
    correo_alterno = models.EmailField("Correo alterno", blank=True)

    # Foto
    foto = models.ImageField(upload_to="miembros/%Y/%m/", blank=True, null=True)

    # Cargo actual (asignable), histórico aparte
    cargo_actual = models.ForeignKey(
        "accounts.Cargo",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="titulares"
    )

    # Campos de Django
    USERNAME_FIELD = "email"
    # Incluye numero_registro para que lo pida en createsuperuser;
    # rls también se puede pedir aquí porque ya lo normalizamos a rls_id en el manager
    REQUIRED_FIELDS = ["first_name", "last_name", "numero_registro", "rls"]

    objects = UserManager()

    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        ordering = ["rls", "last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.numero_registro})"


# ----------------------------------------
# CARGOS e HISTÓRICO
# ----------------------------------------
class Cargo(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self): return self.nombre


class CargoHistorico(models.Model):
    miembro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cargos_hist")
    rls = models.ForeignKey("rls.RLS", on_delete=models.PROTECT, related_name="cargos_hist_accounts")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Cargo histórico"
        verbose_name_plural = "Cargos históricos"
        ordering = ["-fecha_inicio"]
        constraints = [
            models.UniqueConstraint(
                fields=["miembro"],
                condition=models.Q(fecha_fin__isnull=True),
                name="un_cargo_vigente_por_miembro_accounts",
            )
        ]


# ----------------------------------------
# BENEFICIARIOS (máx 3)
# ----------------------------------------
class Beneficiario(models.Model):
    REL = [("conyuge","Cónyuge"),("hijo","Hijo/a"),("padre","Padre/Madre"),("otro","Otro")]
    miembro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="beneficiarios")
    nombre = models.CharField(max_length=120)
    primer_apellido = models.CharField(max_length=120)
    segundo_apellido = models.CharField(max_length=120, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    domicilio = models.TextField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    relacion = models.CharField(max_length=20, choices=REL)
    porcentaje = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Beneficiario"
        verbose_name_plural = "Beneficiarios"

    def clean(self):
        if self.pk is None and self.miembro.beneficiarios.count() >= 3:
            raise ValidationError("Máximo 3 beneficiarios por miembro.")
