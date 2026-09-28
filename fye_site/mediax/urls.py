# mediax/urls.py
#from django.urls import path
#from . import views

#app_name = "mediax"
#urlpatterns = [

#    path("docs/", views.DocumentoListView.as_view(), name="doc_list"),
#    path("docs/nuevo/", views.DocumentoCreateView.as_view(), name="doc_create"),
#    path("imgs/", views.ImagenListView.as_view(), name="img_list"),
#    path("imgs/nueva/", views.ImagenCreateView.as_view(), name="img_create"),
#    path("doc/<int:pk>/privado/", views.documento_privado, name="doc_privado"),
#]
##### ASI LO TENIA 

# mediax/urls.py
# B:\desarrollo\FeyEsp2.0\fye_site\mediax\urls.py
from django.urls import path
from .views import MediaListView, MediaCreateView, MediaDetailView

app_name = "mediax"

urlpatterns = [
    path("",          MediaListView.as_view(),   name="list"),
    path("docs/",     MediaListView.as_view(),   name="doc_list"),  # <- alias para el dashboard
    path("images/",   MediaListView.as_view(),   name="img_list"),   # <— NUEVO alias
    path("new/",      MediaCreateView.as_view(), name="create"),
    path("<int:pk>/", MediaDetailView.as_view(), name="detail"),
]
