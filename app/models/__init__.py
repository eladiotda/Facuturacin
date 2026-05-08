"""Paquete para entidades ORM y relaciones."""

from app.models.cliente import Cliente
from app.models.detalle_factura import DetalleFactura
from app.models.factura import Factura
from app.models.producto import Producto

__all__ = ["Cliente", "DetalleFactura", "Factura", "Producto"]
