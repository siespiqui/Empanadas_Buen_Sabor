from django.urls import path
from .views import lista_productos

app_name = 'productos'

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
]