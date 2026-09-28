# accounts/management/commands/reset_password.py
"""
Restablece (o fija) la contrasena de un usuario, identificandolo por email
o por numero de registro.

Uso:
    # Genera una contrasena segura aleatoria y la muestra en pantalla:
    python manage.py reset_password correo@ejemplo.com

    # Fija una contrasena especifica que tu elijas:
    python manage.py reset_password correo@ejemplo.com --password "MiClaveNueva123!"

    # Tambien funciona buscando por numero de registro:
    python manage.py reset_password USR-ABC12345
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

User = get_user_model()


class Command(BaseCommand):
    help = "Restablece la contrasena de un usuario (por email o numero de registro)."

    def add_arguments(self, parser):
        parser.add_argument(
            "identificador",
            help="Email o numero de registro del usuario a modificar.",
        )
        parser.add_argument(
            "--password",
            default=None,
            help="Nueva contrasena a fijar. Si se omite, se genera una segura al azar.",
        )

    def handle(self, *args, **options):
        identificador = options["identificador"]
        try:
            user = User.objects.get(email__iexact=identificador)
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(numero_registro__iexact=identificador)
            except ObjectDoesNotExist:
                raise CommandError(
                    f"No se encontro ningun usuario con email o numero de registro '{identificador}'."
                )

        nueva_password = options["password"] or get_random_string(
            14, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789!@#$%"
        )

        user.set_password(nueva_password)
        user.save(update_fields=["password"])

        self.stdout.write(self.style.SUCCESS(f"Contrasena actualizada para: {user.email} ({user.numero_registro})"))
        if not options["password"]:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("Nueva contrasena generada (guardala, no se volvera a mostrar):"))
            self.stdout.write(self.style.MIGRATE_HEADING(f"  {nueva_password}"))
            self.stdout.write("")
            self.stdout.write("Comparte esta contrasena con el hermano por un medio seguro y pidele cambiarla al iniciar sesion.")
