# rls/urls.py
from django.urls import path
from .views import RLSListView, RLSCreateView, RLSDetailView

app_name = "rls"

urlpatterns = [
    path("", RLSListView.as_view(), name="list"),
    path("new/", RLSCreateView.as_view(), name="create"),
    path("<int:pk>/", RLSDetailView.as_view(), name="detail"),
]
