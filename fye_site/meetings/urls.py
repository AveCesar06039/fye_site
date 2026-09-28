# meetings/urls.py

from django.urls import path

from .views import TenidaListView, TenidaCreateView, TenidaUpdateView

app_name = "meetings"

urlpatterns = [
    path('', TenidaListView.as_view(), name='tenida_list'),
    #Crear nueva (ESTA ES LA QUE DABA ERROR)
    path('nueva/', TenidaCreateView.as_view(), name='tenida_create'),
    path('asistencia/<int:pk>/', TenidaUpdateView.as_view(), name='tenida_edit'),
]
