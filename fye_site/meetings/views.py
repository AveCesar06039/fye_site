# meetings/views.py
from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy # Importante: agregamos 'reverse'
from django.shortcuts import redirect
from .models import Tenida
from .forms import TenidaForm, AsistenciaFormSet

# 1. Vista para ver el historial de Tenidas
class TenidaListView(ListView):
    model = Tenida
    template_name = 'meetings/tenida_list.html'
    context_object_name = 'tenidas'

# 2. Vista para CREAR la Tenida (Datos básicos)
class TenidaCreateView(CreateView):
    model = Tenida
    form_class = TenidaForm
    template_name = 'meetings/tenida_create.html' 

    def get_success_url(self):
        #  Agregamos 'meetings:' antes de 'tenida_edit'
        # Esto redirige a la toma de lista inmediatamente después de crear la fecha
        return reverse('meetings:tenida_edit', kwargs={'pk': self.object.pk})

# 3. Vista para "Tomar Lista" (Edición masiva con Formset)
class TenidaUpdateView(UpdateView):
    model = Tenida
    form_class = TenidaForm
    template_name = 'meetings/tenida_form.html'
    
    # Agregamos 'meetings:' antes de 'tenida_list'
    success_url = reverse_lazy('meetings:tenida_list') 

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['asistencias'] = AsistenciaFormSet(self.request.POST, instance=self.object)
        else:
            data['asistencias'] = AsistenciaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        asistencias = context['asistencias']
        self.object = form.save()
        if asistencias.is_valid():
            asistencias.save()
            return super().form_valid(form)
        else:
            # Si hay errores en la lista, volvemos a mostrar el formulario
            return self.render_to_response(self.get_context_data(form=form))