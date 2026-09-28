# fye_site/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views  # home publico (renderiza templates/index.html)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Sitio publico institucional
    path("", views.home, name="home"),

    # Panel privado (requiere login)
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Apps
    path("miembros/", include(("miembros.urls", "miembros"), namespace="miembros")),
    path("meetings/", include(("meetings.urls", "meetings"), namespace="meetings")),
    path("finance/", include(("finance.urls", "finance"), namespace="finance")),
    path("media/", include(("mediax.urls", "mediax"), namespace="mediax")),
    path("rls/", include(("rls.urls", "rls"), namespace="rls")),
    path("accounts/", include("allauth.urls")),  # login/logout/reset de password (django-allauth)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
