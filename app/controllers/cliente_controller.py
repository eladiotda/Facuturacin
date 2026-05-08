import re

from app.extensions import db
from app.models import Cliente
from app.controllers.exceptions import ConflictError, ValidationError


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ClienteController:
    @staticmethod
    def _normalize_value(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @staticmethod
    def _validate_required_fields(data: dict) -> None:
        nombre = ClienteController._normalize_value(data.get("nombre"))
        correo = ClienteController._normalize_value(data.get("correo"))

        if not nombre:
            raise ValidationError("El campo nombre es obligatorio")
        if not correo:
            raise ValidationError("El campo correo es obligatorio")
        if not EMAIL_PATTERN.match(correo):
            raise ValidationError("El correo no tiene un formato valido")

    @staticmethod
    def _validate_optional_email(correo: str | None) -> None:
        if correo is not None and not EMAIL_PATTERN.match(correo):
            raise ValidationError("El correo no tiene un formato valido")

    @staticmethod
    def _ensure_unique_email(correo: str, cliente_id: int | None = None) -> None:
        existing_cliente = Cliente.query.filter_by(correo=correo).first()
        if existing_cliente is None:
            return
        if cliente_id is not None and existing_cliente.id == cliente_id:
            return
        raise ConflictError("Ya existe un cliente con ese correo")

    @staticmethod
    def list_clientes() -> list[Cliente]:
        return Cliente.query.order_by(Cliente.id.asc()).all()

    @staticmethod
    def get_cliente(cliente_id: int) -> Cliente | None:
        return db.session.get(Cliente, cliente_id)

    @staticmethod
    def create_cliente(data: dict) -> Cliente:
        ClienteController._validate_required_fields(data)

        nombre = ClienteController._normalize_value(data["nombre"])
        correo = ClienteController._normalize_value(data["correo"])
        telefono = ClienteController._normalize_value(data.get("telefono"))
        direccion = ClienteController._normalize_value(data.get("direccion"))

        ClienteController._ensure_unique_email(correo)

        cliente = Cliente(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
        )
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def update_cliente(cliente: Cliente, data: dict) -> Cliente:
        if "nombre" in data:
            nombre = ClienteController._normalize_value(data.get("nombre"))
            if not nombre:
                raise ValidationError("El campo nombre no puede estar vacio")
            cliente.nombre = nombre

        if "correo" in data:
            correo = ClienteController._normalize_value(data.get("correo"))
            if not correo:
                raise ValidationError("El campo correo no puede estar vacio")
            ClienteController._validate_optional_email(correo)
            ClienteController._ensure_unique_email(correo, cliente.id)
            cliente.correo = correo

        if "telefono" in data:
            cliente.telefono = ClienteController._normalize_value(data.get("telefono"))

        if "direccion" in data:
            cliente.direccion = ClienteController._normalize_value(data.get("direccion"))

        db.session.commit()
        return cliente

    @staticmethod
    def delete_cliente(cliente: Cliente) -> None:
        db.session.delete(cliente)
        db.session.commit()
