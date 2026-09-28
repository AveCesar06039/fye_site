from django.apps import AppConfig

class MiembrosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "miembros"           # <— ¡nombre del paquete, NO 'members'!
    verbose_name = "Miembros"
