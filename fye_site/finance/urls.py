from django.urls import path
from .views import PagoListView, PagoCreateView, PagoDetailView

app_name = "finance"

urlpatterns = [
    path("", PagoListView.as_view(), name="pago_list"),
    path("crear/", PagoCreateView.as_view(), name="pago_create"),
    path("<int:pk>/", PagoDetailView.as_view(), name="pago_detail"),
]
