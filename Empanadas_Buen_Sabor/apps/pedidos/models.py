from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto

class Pedido(models.Model):
    """
    Cabecera de la orden de compra/pedido
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente de Pago / Confirmación'),
        ('EN_PREPARACION', 'En Cocina / Preparación'),
        ('LISTO', 'Listo para Despacho'),
        ('EN_TRAYECTO', 'En Camino (Domicilio)'),
        ('ENTREGADO', 'Entregado al Cliente'),
        ('CANCELADO', 'Pedido Cancelado'),
    )

    METODOS_PAGO = (
        ('NEQUI', 'Nequi / Daviplata (Transferencia QR)'),
        ('CONTRA_ENTREGA', 'Pago Contra Entrega (Efectivo)'),
    )

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos', verbose_name="Cliente")
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE', verbose_name="Estado del Pedido")
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, verbose_name="Método de Pago")
    
    # Datos de envío
    direccion_entrega = models.CharField(max_length=255, verbose_name="Dirección de Domicilio")
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    notas_adicionales = models.TextField(blank=True, null=True, verbose_name="Instrucciones para el Domiciliario")
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total a Pagar ($)")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username} ({self.get_estado_display()})"


class DetallePedido(models.Model):
    """
    Productos individuales incluidos en el pedido
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles', verbose_name="Pedido")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario ($)")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal ($)")

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles de los Pedidos"

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"