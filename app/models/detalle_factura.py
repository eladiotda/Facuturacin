from decimal import Decimal

from app.extensions import db


class DetalleFactura(db.Model):
    __tablename__ = "detalle_factura"

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey("facturas.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    subtotal = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    factura = db.relationship("Factura", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles_factura")

    def __repr__(self) -> str:
        return f"<DetalleFactura factura={self.factura_id} producto={self.producto_id}>"
