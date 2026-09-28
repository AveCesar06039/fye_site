# B:\desarrollo\FeyEsp2.0\fye_site\meetings\admin.py
from django.contrib import admin
from .models import Tenida, Asistencia

# Esta clase crea la "Tabla" dentro de la Tenida
class AsistenciaInline(admin.TabularInline):
    model = Asistencia
    extra = 0 # Muestra 1 renglón vacío para agregar rápido
    #autocomplete_fields = ['miembro'] # Vital si tienes muchos miembros
    fields = ('miembro', 'puesto', 'presente', 'observaciones')
    verbose_name = "Asistencia del Hermano"
    verbose_name_plural = "Pase de Lista (Tabla de Asistencia)"

@admin.register(Tenida)
class TenidaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'grado', 'rls', 'conteo_asistencia')
    list_filter = ('fecha', 'tipo', 'rls')
    search_fields = ('tema',)
    
    # Aquí conectamos la tabla
    inlines = [AsistenciaInline]

    def conteo_asistencia(self, obj):
        return obj.asistencias.filter(presente=True).count()
    conteo_asistencia.short_description = "Asistentes"

# Opcional: Si quieres ver las asistencias sueltas también
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('tenida', 'miembro', 'puesto', 'presente')
    list_filter = ('tenida__fecha', 'puesto','presente')