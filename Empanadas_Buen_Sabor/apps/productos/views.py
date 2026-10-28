from django.shortcuts import render
from .models import Producto

def lista_productos(request):
    """
    Vista para listar los productos disponibles en el catálogo del index
    """
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'index.html', {'productos': productos})