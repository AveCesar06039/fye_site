# accounts/management/commands/list_users.py
"""
Lista los usuarios (hermanos) registrados en el sistema.

Uso:
    python manage.py list_users
    python manage.py list_users --solo-activos
    python manage.py list_users --solo-sin-password
"""
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Lista los usuarios del sistema (email, numero de registro, rol, estado de la contraseña)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--solo-activos",
            action="store_true",
            help="Muestra solo usuarios con is_active=True.",
        )
        parser.add_argument(
            "--solo-sin-password",
            action="store_true",
            help="Muestra solo usuarios sin contraseña utilizable (no pueden iniciar sesion).",
        )

    def handle(self, *args, **options):
        qs = User.objects.all().order_by("email")
        if options["solo_activos"]:
            qs = qs.filter(is_active=True)

        filas = []
        for u in qs:
            tiene_password = u.has_usable_password()
            if options["solo_sin_password"] and tiene_password:
                continue
            rol = (
                "superusuario" if u.is_superuser
                else "staff" if u.is_staff
                else "hermano"
            )
            filas.append((
                u.email,
                u.numero_registro,
                f"{u.first_name} {u.last_name}".strip(),
                rol,
                "activo" if u.is_active else "INACTIVO",
                "OK" if tiene_password else "SIN CONTRASENA",
                u.last_login.strftime("%Y-%m-%d %H:%M") if u.last_login else "nunca",
            ))

        if not filas:
            self.stdout.write(self.style.WARNING("No se encontraron usuarios con esos filtros."))
            return

        encabezados = ("EMAIL", "NUM. REGISTRO", "NOMBRE", "ROL", "ESTADO", "PASSWORD", "ULTIMO LOGIN")
        anchos = [max(len(str(f[i])) for f in ([encabezados] + filas)) for i in range(len(encabezados))]

        def fmt(fila):
            return "  ".join(str(v).ljust(anchos[i]) for i, v in enumerate(fila))

        self.stdout.write(self.style.MIGRATE_HEADING(fmt(encabezados)))
        self.stdout.write("-" * (sum(anchos) + 2 * (len(anchos) - 1)))
        for fila in filas:
            self.stdout.write(fmt(fila))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Total: {len(filas)} usuario(s)."))
