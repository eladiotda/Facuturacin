from decimal import Decimal

from app.controllers.exceptions import ValidationError
from app.extensions import db
from app.models import Cliente, DetalleFactura, Factura, Producto


class FacturaController:
    @staticmethod
    def _normalize_value(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @staticmethod
    def _validate_factura_payload(data: dict) -> tuple[str, int, list[dict]]:
        numero = FacturaController._normalize_value(data.get("numero"))
        cliente_id = data.get("cliente_id")
        detalles = data.get("detalles")

        if not numero:
            raise ValidationError("El campo numero es obligatorio")
        if cliente_id is None:
            raise ValidationError("El campo cliente_id es obligatorio")
        if not isinstance(detalles, list) or not detalles:
            raise ValidationError("La factura debe incluir al menos un detalle")

        try:
            cliente_id = int(cliente_id)
        except (TypeError, ValueError):
            raise ValidationError("El cliente_id debe ser un numero entero") from None

        return numero, cliente_id, detalles

    @staticmethod
    def _validate_detail(detail: dict) -> tuple[int, Producto, int, Decimal]:
        producto_id = detail.get("producto_id")
        cantidad = detail.get("cantidad")

        if producto_id is None:
            raise ValidationError("Cada detalle debe incluir producto_id")
        if cantidad is None:
            raise ValidationError("Cada detalle debe incluir cantidad")

        try:
            producto_id = int(producto_id)
        except (TypeError, ValueError):
            raise ValidationError("El producto_id debe ser un numero entero") from None

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValidationError("La cantidad debe ser un numero entero") from None

        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero")

        producto = db.session.get(Producto, producto_id)
        if producto is None:
            raise ValidationError(f"El producto con id {producto_id} no existe")
        if producto.stock < cantidad:
            raise ValidationError(
                f"Stock insuficiente para el producto {producto.nombre}"
            )

        precio_unitario = producto.precio.quantize(Decimal("0.01"))
        return producto_id, producto, cantidad, precio_unitario

    @staticmethod
    def list_facturas() -> list[Factura]:
        return Factura.query.order_by(Factura.id.asc()).all()

    @staticmethod
    def get_factura(factura_id: int) -> Factura | None:
        return db.session.get(Factura, factura_id)

    @staticmethod
    def create_factura(data: dict) -> Factura:
        numero, cliente_id, detalles_payload = FacturaController._validate_factura_payload(data)

        existing_factura = Factura.query.filter_by(numero=numero).first()
        if existing_factura is not None:
            raise ValidationError("Ya existe una factura con ese numero")

        cliente = db.session.get(Cliente, cliente_id)
        if cliente is None:
            raise ValidationError(f"El cliente con id {cliente_id} no existe")

        factura = Factura(numero=numero, cliente=cliente, total=Decimal("0.00"))
        db.session.add(factura)
        total = Decimal("0.00")
        used_product_ids: set[int] = set()

        for detail in detalles_payload:
            producto_id, producto, cantidad, precio_unitario = FacturaController._validate_detail(detail)
            if producto_id in used_product_ids:
                raise ValidationError(
                    f"El producto con id {producto_id} no puede repetirse en la factura"
                )
            used_product_ids.add(producto_id)

            subtotal = (precio_unitario * cantidad).quantize(Decimal("0.01"))

            factura.detalles.append(
                DetalleFactura(
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal,
                )
            )

            producto.stock -= cantidad
            total += subtotal

        factura.total = total.quantize(Decimal("0.01"))
        db.session.commit()
        return factura
