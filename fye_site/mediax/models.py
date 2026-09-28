# B:\desarrollo\FeyEsp2.0\fye_site\mediax\models.py
from django.db import models
from django.contrib.auth import get_user_model
# mediax/models.py
import datetime

# Compat para migraciones antiguas que usan mediax.models.doc_path
def doc_path(instance, filename):
    # cualquier ruta estable; no importa que no sea exactamente igual a la original,
    # solo que exista y devuelva un string
    today = datetime.date.today()
    return f"uploads/{today.year}/{today.month:02d}/{filename}"


User = get_user_model()

class MediaItem(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Público'),
        ('STAFF',  'Solo staff'),
    ]

    file = models.FileField(upload_to='uploads/%Y/%m/')
    title = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')  # <- OJO: CHOICES bien escrito

    def __str__(self):
        return self.title or self.file.name
# --- Compat para migraciones antiguas que usan upload_to callables ---
import datetime

def doc_path(instance, filename):
    """Compat: usado por 0001_initial. Devuelve una ruta estable."""
    today = datetime.date.today()
    return f"uploads/{today.year}/{today.month:02d}/{filename}"

def img_path(instance, filename):
    """Compat: usado por 0001_initial. Devuelve una ruta estable."""
    today = datetime.date.today()
    # si quieres separarlo por modelo:
    model = instance.__class__.__name__.lower() if instance else "misc"
    return f"images/{model}/{today.year}/{today.month:02d}/{filename}"
# --------------------------------------------------------------------
