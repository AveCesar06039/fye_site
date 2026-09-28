from django.urls import path
from . import views
app_name = "miembros"

urlpatterns = [
    path("", views.MiembroListView.as_view(), name="list"),
    path("nuevo/", views.MiembroCreateView.as_view(), name="create"),
    path("<int:pk>/", views.MiembroDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.MiembroUpdateView.as_view(), name="update"),
    # Beneficiarios
    path("<int:pk>/beneficiarios/", views.BeneficiarioListCreateView.as_view(), name="benef_list_create"),
]
