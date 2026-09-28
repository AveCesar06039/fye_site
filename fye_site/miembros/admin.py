from django.contrib import admin
from .models import Member, Beneficiario, Cargo, CargoHistorico
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Member)
class MemberAdmin(SimpleHistoryAdmin):
    list_display = ("numero_registro","nombre","primer_apellido","rls","grado","estado")
    list_filter = ("rls","grado","estado")
    search_fields = ("numero_registro","nombre","primer_apellido","segundo_apellido","correo_electronico")

admin.site.register(Beneficiario)
admin.site.register(Cargo)
admin.site.register(CargoHistorico)
