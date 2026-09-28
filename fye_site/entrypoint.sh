#!/bin/sh
set -e

echo ">> Aplicando migraciones..."
python manage.py migrate --noinput

echo ">> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo ">> Verificando superusuario inicial..."
python manage.py shell -c "
from accounts.models import User
import os

email = os.environ.get('ADMIN_EMAIL')
password = os.environ.get('ADMIN_PASSWORD')

if email and password:
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            email=email,
            password=password,
            first_name='Admin',
            last_name='Admin',
        )
        print('Superusuario creado:', email)
    else:
        print('El superusuario ya existe:', email)
else:
    print('ADMIN_EMAIL / ADMIN_PASSWORD no definidos, se omite creación de superusuario.')
"

echo ">> Iniciando gunicorn..."
exec gunicorn fye_site.wsgi:application --bind 0.0.0.0:${PORT:-8000}
