# dashboard/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from miembros.models import Member
from rls.models import RLS
from meetings.models import Tenida


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 🔹 KPI Miembros
        ctx["kpi_miembros_activos"] = Member.objects.filter(estado="ACT").count()
        ctx["kpi_miembros_suenos"] = Member.objects.filter(estado="SUE").count()
        ctx["kpi_total_miembros"] = Member.objects.count()

        # 🔹 KPI RLS
        ctx["kpi_total_rls"] = RLS.objects.count()

        # 🔹 KPI Tenidas del año actual
        year = timezone.now().year
        ctx["kpi_tenidas_ano"] = Tenida.objects.filter(fecha__year=year).count()

        return ctx
