# B:\desarrollo\FeyEsp2.0\fye_site\mediax\views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import MediaItem
from .forms import MediaItemForm

class MediaListView(LoginRequiredMixin, ListView):
    template_name = "mediax/list.html"
    model = MediaItem
    context_object_name = "items"
    paginate_by = 20
    ordering = ["-created_at"]

class MediaCreateView(LoginRequiredMixin, CreateView):
    template_name = "mediax/form.html"
    model = MediaItem
    form_class = MediaItemForm
    success_url = reverse_lazy("mediax:list")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class MediaDetailView(LoginRequiredMixin, DetailView):
    template_name = "mediax/detail.html"
    model = MediaItem
    context_object_name = "item"
