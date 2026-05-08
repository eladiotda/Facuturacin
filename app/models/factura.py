from datetime import UTC, datetime
from decimal import Decimal

from app.extensions import db


class Factura(db.Model):
    __tablename__ = "facturas"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False, unique=True)
    fecha_emision = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    cliente = db.relationship("Cliente", back_populates="facturas")
    detalles = db.relationship(
        "DetalleFactura",
        back_populates="factura",
        lazy=True,
        cascade="all, delete-orphan",
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    def __repr__(self) -> str:
        return f"<Factura {self.numero}>"
