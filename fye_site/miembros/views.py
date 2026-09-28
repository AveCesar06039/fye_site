# miembros/views.py

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
    # Q se usa en el listado
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Member, Beneficiario, Cargo
from .forms import MemberForm, BeneficiarioFormSet
from rls.models import RLS


# ─────────────────────────────────────────────
# LISTADO DE MIEMBROS
# ─────────────────────────────────────────────
class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "miembros/list.html"
    context_object_name = "miembros"
    paginate_by = 25

    def get_queryset(self):
        qs = Member.objects.select_related("rls", "cargo_actual")

        q = self.request.GET.get("q")
        grado = self.request.GET.get("grado")
        estado = self.request.GET.get("estado")
        rls_id = self.request.GET.get("rls")
        order_param = self.request.GET.get("order")

        # 🔍 Búsqueda de texto
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(primer_apellido__icontains=q)
                | Q(segundo_apellido__icontains=q)
                | Q(numero_registro__icontains=q)
            )

        # 🎓 Filtro por grado
        if grado:
            qs = qs.filter(grado=grado)

        # 💤 / ✅ Filtro por estado
        if estado:
            qs = qs.filter(estado=estado)

        # 🏛️ Filtro por RLS
        if rls_id:
            qs = qs.filter(rls_id=rls_id)

        # ↕️ Ordenamiento permitido
        allowed_orders = {
            "nombre": "nombre",
            "-nombre": "-nombre",
            "apellido": "primer_apellido",
            "-apellido": "-primer_apellido",
            "numero_registro": "numero_registro",
            "-numero_registro": "-numero_registro",
            "grado": "grado",
            "-grado": "-grado",
            "estado": "estado",
            "-estado": "-estado",
            "rls": "rls__nombre",
            "-rls": "-rls__nombre",
        }

        if order_param in allowed_orders:
            qs = qs.order_by(allowed_orders[order_param], "primer_apellido", "nombre")
        else:
            qs = qs.order_by("rls__nombre", "primer_apellido", "nombre")

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filtros"] = {
            "q": self.request.GET.get("q", ""),
            "grado": self.request.GET.get("grado", ""),
            "estado": self.request.GET.get("estado", ""),
            "rls": self.request.GET.get("rls", ""),
            "order": self.request.GET.get("order", ""),
        }
        # Choices desde el modelo
        ctx["GRADO_CHOICES"] = Member._meta.get_field("grado").choices
        ctx["ESTADO_CHOICES"] = Member._meta.get_field("estado").choices
        ctx["rls_list"] = RLS.objects.all().order_by("nombre")
        return ctx


# ─────────────────────────────────────────────
# CREAR MIEMBRO
# ─────────────────────────────────────────────
class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "miembros/form.html"
    success_url = reverse_lazy("miembros:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["benef_formset"] = BeneficiarioFormSet(
                self.request.POST,
                self.request.FILES,
            )
        else:
            ctx["benef_formset"] = BeneficiarioFormSet()
        return ctx

    def form_valid(self, form):
        """
        Guarda el miembro, crea usuario (si se marcó la casilla)
        y guarda beneficiarios.
        """
        context = self.get_context_data()
        benef_formset = context["benef_formset"]

        if form.is_valid() and benef_formset.is_valid():
            # Guardar miembro (aquí se genera numero_registro en save())
            self.object = form.save()

            # Lógica de creación de usuario
            crear_usuario = form.cleaned_data.get("crear_usuario")
            email = form.cleaned_data.get("correo_electronico")
            pwd1 = form.cleaned_data.get("password1")

            if crear_usuario and email and pwd1:
                User = get_user_model()
                user = None

                # Intentar primero el patrón de usuario con email como USERNAME_FIELD
                try:
                    user = User.objects.create_user(email=email, password=pwd1)
                except TypeError:
                    # Fallback al usuario clásico con username + email
                    username = email or self.object.numero_registro or f"miembro_{User.objects.count() + 1}"
                    user = User.objects.create_user(
                        username=username,
                        email=email or "",
                        password=pwd1,
                    )

                self.object.user = user
                self.object.save()

            # Guardar beneficiarios
            benef_formset.instance = self.object
            benef_formset.save()

            messages.success(self.request, "Miembro creado correctamente.")
            return redirect(self.get_success_url())

        return self.form_invalid(form)


# ─────────────────────────────────────────────
# EDITAR MIEMBRO
# ─────────────────────────────────────────────
class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "miembros/form.html"
    success_url = reverse_lazy("miembros:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["benef_formset"] = BeneficiarioFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
            )
        else:
            ctx["benef_formset"] = BeneficiarioFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        """
        Guarda cambios del miembro + beneficiarios.
        No vuelve a crear usuario; solo actualiza datos del miembro.
        """
        context = self.get_context_data()
        benef_formset = context["benef_formset"]

        if form.is_valid() and benef_formset.is_valid():
            self.object = form.save()
            benef_formset.instance = self.object
            benef_formset.save()

            messages.success(self.request, "Miembro actualizado correctamente.")
            return redirect(self.get_success_url())

        return self.form_invalid(form)


# ─────────────────────────────────────────────
# DETALLE DE MIEMBRO
# ─────────────────────────────────────────────
class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "miembros/detail.html"
    context_object_name = "obj"


# ─────────────────────────────────────────────
# ELIMINAR MIEMBRO
# ─────────────────────────────────────────────
class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "miembros/confirm_delete.html"
    success_url = reverse_lazy("miembros:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Miembro eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ─────────────────────────────────────────────
# CRUD DE CARGOS
# ─────────────────────────────────────────────
class CargoCreateView(LoginRequiredMixin, CreateView):
    model = Cargo
    fields = ["nombre", "descripcion", "activo"]
    template_name = "miembros/cargo_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse_lazy("miembros:list")


class CargoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cargo
    fields = ["nombre", "descripcion", "activo"]
    template_name = "miembros/cargo_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse_lazy("miembros:list")


class CargoDeleteView(LoginRequiredMixin, DeleteView):
    model = Cargo
    template_name = "miembros/cargo_confirm_delete.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse_lazy("miembros:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Cargo eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
