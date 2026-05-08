from app.extensions import db
from app.models import Cliente


class ClienteController:
    @staticmethod
    def list_clientes() -> list[Cliente]:
        return Cliente.query.order_by(Cliente.id.asc()).all()

    @staticmethod
    def get_cliente(cliente_id: int) -> Cliente | None:
        return db.session.get(Cliente, cliente_id)

    @staticmethod
    def create_cliente(data: dict) -> Cliente:
        cliente = Cliente(
            nombre=data["nombre"],
            correo=data["correo"],
            telefono=data.get("telefono"),
            direccion=data.get("direccion"),
        )
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def update_cliente(cliente: Cliente, data: dict) -> Cliente:
        cliente.nombre = data.get("nombre", cliente.nombre)
        cliente.correo = data.get("correo", cliente.correo)
        cliente.telefono = data.get("telefono", cliente.telefono)
        cliente.direccion = data.get("direccion", cliente.direccion)
        db.session.commit()
        return cliente

    @staticmethod
    def delete_cliente(cliente: Cliente) -> None:
        db.session.delete(cliente)
        db.session.commit()
