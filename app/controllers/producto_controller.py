from decimal import Decimal, InvalidOperation

from app.controllers.exceptions import ConflictError, ValidationError
from app.extensions import db
from app.models import Producto


class ProductoController:
    @staticmethod
    def _normalize_value(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @staticmethod
    def _parse_precio(value) -> Decimal:
        try:
            precio = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError("El precio debe ser un numero valido") from None

        if precio < 0:
            raise ValidationError("El precio no puede ser negativo")

        return precio.quantize(Decimal("0.01"))

    @staticmethod
    def _parse_stock(value) -> int:
        try:
            stock = int(value)
        except (TypeError, ValueError):
            raise ValidationError("El stock debe ser un numero entero") from None

        if stock < 0:
            raise ValidationError("El stock no puede ser negativo")

        return stock

    @staticmethod
    def _validate_required_fields(data: dict) -> None:
        nombre = ProductoController._normalize_value(data.get("nombre"))

        if not nombre:
            raise ValidationError("El campo nombre es obligatorio")
        if "precio" not in data:
            raise ValidationError("El campo precio es obligatorio")
        if "stock" not in data:
            raise ValidationError("El campo stock es obligatorio")

    @staticmethod
    def _ensure_unique_nombre(nombre: str, producto_id: int | None = None) -> None:
        existing_producto = Producto.query.filter_by(nombre=nombre).first()
        if existing_producto is None:
            return
        if producto_id is not None and existing_producto.id == producto_id:
            return
        raise ConflictError("Ya existe un producto con ese nombre")

    @staticmethod
    def list_productos() -> list[Producto]:
        return Producto.query.order_by(Producto.id.asc()).all()

    @staticmethod
    def get_producto(producto_id: int) -> Producto | None:
        return db.session.get(Producto, producto_id)

    @staticmethod
    def create_producto(data: dict) -> Producto:
        ProductoController._validate_required_fields(data)

        nombre = ProductoController._normalize_value(data["nombre"])
        precio = ProductoController._parse_precio(data["precio"])
        stock = ProductoController._parse_stock(data["stock"])

        ProductoController._ensure_unique_nombre(nombre)

        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
        )
        db.session.add(producto)
        db.session.commit()
        return producto

    @staticmethod
    def update_producto(producto: Producto, data: dict) -> Producto:
        if "nombre" in data:
            nombre = ProductoController._normalize_value(data.get("nombre"))
            if not nombre:
                raise ValidationError("El campo nombre no puede estar vacio")
            ProductoController._ensure_unique_nombre(nombre, producto.id)
            producto.nombre = nombre

        if "precio" in data:
            producto.precio = ProductoController._parse_precio(data["precio"])

        if "stock" in data:
            producto.stock = ProductoController._parse_stock(data["stock"])

        db.session.commit()
        return producto

    @staticmethod
    def delete_producto(producto: Producto) -> None:
        db.session.delete(producto)
        db.session.commit()
