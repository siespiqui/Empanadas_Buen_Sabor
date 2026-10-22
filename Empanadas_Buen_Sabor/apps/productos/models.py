from django.db import models

class Categoria(models.Model):
    """
    Categorías de productos (ej: Empanadas Tradicionales, Especiales, Bebidas, Combos)
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    estado = models.BooleanField(default=True, verbose_name="¿Categoría Activa?")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Catálogo de Empanadas y Acompañamientos
    """
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos', verbose_name="Categoría")
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre de la Empanada/Producto")
    descripcion = models.TextField(verbose_name="Ingredientes y Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario ($)")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Foto del Producto")
    disponible = models.BooleanField(default=True, verbose_name="¿Disponible para Venta?")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"