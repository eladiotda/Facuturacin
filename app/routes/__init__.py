"""Paquete para endpoints REST del sistema."""

from app.routes.cliente_routes import clientes_bp
from app.routes.factura_routes import facturas_bp
from app.routes.producto_routes import productos_bp

__all__ = ["clientes_bp", "facturas_bp", "productos_bp"]
