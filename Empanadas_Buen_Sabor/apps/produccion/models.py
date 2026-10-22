from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto

class LoteProduccion(models.Model):
    """
    Registro de lotes de empanadas fabricados en cocina
    """
    ESTADOS_LOTE = (
        ('EN_PROCESO', 'En Proceso de Elaboración'),
        ('FINALIZADO', 'Finalizado / Listo para Inventario'),
        ('CANCELADO', 'Lote Cancelado'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto Fabricado")
    cantidad_producida = models.PositiveIntegerField(verbose_name="Cantidad Producida")
    numero_lote = models.CharField(max_length=50, unique=True, verbose_name="Número de Lote")
    estado = models.CharField(max_length=20, choices=ESTADOS_LOTE, default='EN_PROCESO', verbose_name="Estado del Lote")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Responsable de Producción")
    fecha_produccion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de Producción")

    class Meta:
        verbose_name = "Lote de Producción"
        verbose_name_plural = "Lotes de Producción"
        ordering = ['-fecha_produccion']

    def __str__(self):
        return f"Lote #{self.numero_lote} - {self.producto.nombre} ({self.cantidad_producida} unds)"


class Merma(models.Model):
    """
    Control de mermas, pérdidas o empanadas dañadas durante la producción
    """
    lote = models.ForeignKey(LoteProduccion, on_delete=models.CASCADE, related_name='mermas', verbose_name="Lote Asociado")
    cantidad_perdida = models.PositiveIntegerField(verbose_name="Cantidad Dañada / Perdida")
    motivo = models.CharField(max_length=255, verbose_name="Motivo de la Merma (ej: Empanada rota, quemada)")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Merma"
        verbose_name_plural = "Mermas"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"Merma: {self.cantidad_perdida} unds ({self.motivo})"