from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from utils.mixins import RLSScopeMixin
from accounts.models import User, Beneficiario, CargoHistorico

class MiembroListView(RLSScopeMixin, ListView):
    model = User
    paginate_by = 25
    template_name = "miembros/miembro_list.html"
    def get_queryset(self):
        qs = super().get_queryset().select_related("rls","cargo_actual")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(numero_registro__icontains=q) | qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q)
        return qs

class MiembroCreateView(RLSScopeMixin, CreateView):
    model = User
    fields = [
        "rls","email","password","first_name","last_name","second_surname",
        "numero_registro","grado","fecha_iniciacion","estado",
        "numero_celular","correo_alterno","foto","cargo_actual"
    ]
    template_name = "miembros/miembro_form.html"
    success_url = reverse_lazy("miembros:list")

    def dispatch(self, request, *args, **kwargs):
        # Si no hay RLS, obligamos a crear una primero
        from rls.models import RLS
        if not RLS.objects.exists():
            messages.error(request, "Primero debes crear una RLS.")
            return redirect("rls:create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # setea contraseña correctamente
        user = form.save(commit=False)
        raw = form.cleaned_data.get("password")
        if raw:
            user.set_password(raw)
        user.save()
        messages.success(self.request, "Miembro creado.")
        return redirect(self.success_url)

class MiembroUpdateView(RLSScopeMixin, UpdateView):
    model = User
    fields = [
        "rls","email","first_name","last_name","second_surname",
        "numero_registro","grado","fecha_iniciacion","estado",
        "numero_celular","correo_alterno","foto","cargo_actual"
    ]
    template_name = "miembros/miembro_form.html"
    success_url = reverse_lazy("miembros:list")

class MiembroDetailView(RLSScopeMixin, DetailView):
    model = User
    template_name = "miembros/miembro_detail.html"

# ------- Beneficiarios -------
class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ["nombre","primer_apellido","segundo_apellido","fecha_nacimiento","domicilio","telefono","relacion","porcentaje"]

class BeneficiarioListCreateView(RLSScopeMixin, FormView):
    template_name = "miembros/beneficiario_list_create.html"
    form_class = BeneficiarioForm

    def dispatch(self, request, *args, **kwargs):
        self.miembro = get_object_or_404(User, pk=kwargs["pk"])
        if request.user.rls_scope_id and self.miembro.rls_id != request.user.rls_scope_id:
            raise PermissionDenied("Fuera de su RLS.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["miembro"] = self.miembro
        ctx["beneficiarios"] = self.miembro.beneficiarios.all()
        return ctx

    def form_valid(self, form):
        b = form.save(commit=False)
        b.miembro = self.miembro
        b.full_clean()  # valida máximo 3
        b.save()
        return redirect("miembros:benef_list_create", pk=self.miembro.pk)
