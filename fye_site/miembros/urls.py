from django.urls import path
from .views import (
    MemberListView,
    MemberCreateView,
    MemberUpdateView,
    MemberDetailView,
    MemberDeleteView,
    CargoCreateView,
    CargoUpdateView,
    CargoDeleteView,
)

urlpatterns = [
    path("", MemberListView.as_view(), name="list"),
    path("nuevo/", MemberCreateView.as_view(), name="create"),
    path("<int:pk>/", MemberDetailView.as_view(), name="detail"),

    # principal
    path("<int:pk>/editar/", MemberUpdateView.as_view(), name="update"),

    # alias para compatibilidad con 'edit' usado en las plantillas viejas
    path("<int:pk>/edit/", MemberUpdateView.as_view(), name="edit"),

    path("<int:pk>/eliminar/", MemberDeleteView.as_view(), name="delete"),

    # cargos
    path("cargos/nuevo/", CargoCreateView.as_view(), name="cargo_create"),
    path("cargos/<int:pk>/editar/", CargoUpdateView.as_view(), name="cargo_update"),
    path("cargos/<int:pk>/eliminar/", CargoDeleteView.as_view(), name="cargo_delete"),
]
