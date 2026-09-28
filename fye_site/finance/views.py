# B:\desarrollo\FeyEsp2.0\fye_site\finance\views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from utils.mixins import RLSScopeMixin
from .models import Pago
from .forms import PagoForm  # si no existe aún, ver abajo


class PagoListView(LoginRequiredMixin, RLSScopeMixin, ListView):
    model = Pago
    template_name = "finance/list.html"
    context_object_name = "object_list"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        # Si tu modelo Pago tiene campo rls (ForeignKey a RLS)
        qs = self.filter_by_rls(qs, field="rls_id")
        return qs.select_related("miembro", "rls")

class PagoCreateView(LoginRequiredMixin, RLSScopeMixin, CreateView):
    model = Pago
    template_name = "finance/form.html"
    success_url = reverse_lazy("finance:list")
    # usa ModelForm si lo tienes, o bien fields para un formulario simple:
    form_class = PagoForm

    def get_initial(self):
        initial = super().get_initial()
        rid = self.get_rls_id()
        if rid:
            initial["rls"] = rid
        return initial

class PagoDetailView(LoginRequiredMixin, RLSScopeMixin, DetailView):
    model = Pago
    template_name = "finance/detail.html"
    context_object_name = "obj"


#--
class RLSScopeMixin(object):
    def get_rls_id(self):
        user = getattr(self, "request", None) and self.request.user or None
        return getattr(user, "rls_scope_id", None) or getattr(user, "rls_id", None)

    def filter_by_rls(self, qs, field="rls_id"):
        rid = self.get_rls_id()
        return qs.filter(**{field: rid}) if rid else qs