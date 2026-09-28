# rls/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import RLS
from .forms import RLSForm

class RLSListView(LoginRequiredMixin, ListView):
    model = RLS
    template_name = "rls/list.html"
    context_object_name = "object_list"
    ordering = ["nombre", "numero"]

class RLSCreateView(LoginRequiredMixin, CreateView):
    model = RLS
    form_class = RLSForm
    template_name = "rls/form.html"
    success_url = reverse_lazy("rls:list")

class RLSDetailView(LoginRequiredMixin, DetailView):
    model = RLS
    template_name = "rls/detail.html"
    context_object_name = "obj"
