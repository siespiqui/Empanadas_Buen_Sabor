from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    """
    Gestión de proveedores de materias primas e insumos
    """
    nit = models.CharField(max_length=50, unique=True, verbose_name="NIT / Identificación")
    nombre_empresa = models.CharField(max_length=150, verbose_name="Nombre de la Empresa / Proveedor")
    nombre_contacto = models.CharField(max_length=100, verbose_name="Persona de Contacto")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="¿Proveedor Activo?")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre_empresa']

    def __str__(self):
        return f"{self.nombre_empresa} (NIT: {self.nit})"


class OrdenCompra(models.Model):
    """
    Órdenes de compra realizadas a los proveedores para reabastecimiento
    """
    ESTADOS_ORDEN = (
        ('SOLICITADA', 'Orden Solicitada'),
        ('RECIBIDA', 'Recibida en Inventario'),
        ('CANCELADA', 'Orden Cancelada'),
    )

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ordenes_compra', verbose_name="Proveedor")
    numero_factura = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Factura / Remisión")
    fecha_compra = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la Compra")
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Costo Total ($)")
    estado = models.CharField(max_length=20, choices=ESTADOS_ORDEN, default='SOLICITADA', verbose_name="Estado de la Orden")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha_compra']

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre_empresa} (${self.costo_total})"