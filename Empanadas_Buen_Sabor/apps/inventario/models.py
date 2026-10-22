from django.db import models
from django.contrib.auth.models import User

class Insumo(models.Model):
    """
    Materias primas e insumos (Harina, Carne, Papa, Aceite, Empaques, etc.)
    """
    UNIDADES_MEDIDA = (
        ('KG', 'Kilogramos'),
        ('GR', 'Gramos'),
        ('LT', 'Litros'),
        ('ML', 'Militros'),
        ('UND', 'Unidades'),
        ('PAQ', 'Paquetes'),
    )

    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Insumo")
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES_MEDIDA, verbose_name="Unidad de Medida")
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Stock Actual")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, verbose_name="Stock Mínimo (Alerta)")
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo Promedio Unitario ($)")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.get_unidad_medida_display()})"


class MovimientoInventario(models.Model):
    """
    Registro de entradas (compras) y salidas (producción o ajustes) de materia prima
    """
    TIPOS_MOVIMIENTO = (
        ('ENTRADA', 'Entrada por Compra / Reabastecimiento'),
        ('SALIDA', 'Salida por Producción de Empanadas'),
        ('AJUSTE', 'Ajuste de Inventario / Corrección'),
        ('PERDIDA', 'Pérdida / Insumo Danado'),
    )

    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, related_name='movimientos', verbose_name="Insumo")
    tipo_movimiento = models.CharField(max_length=15, choices=TIPOS_MOVIMIENTO, verbose_name="Tipo de Movimiento")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    motivo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Motivo / Observación")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo_movimiento}: {self.cantidad} {self.insumo.unidad_medida} de {self.insumo.nombre}"