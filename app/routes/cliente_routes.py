from flask import Blueprint, request

from app.api.responses import error_response, message_response, success_response
from app.controllers import ClienteController


clientes_bp = Blueprint("clientes", __name__, url_prefix="/api/v1/clientes")


def serialize_cliente(cliente) -> dict:
    return {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion,
        "created_at": cliente.created_at.isoformat(),
        "updated_at": cliente.updated_at.isoformat(),
    }


@clientes_bp.get("")
def list_clientes():
    clientes = ClienteController.list_clientes()
    return success_response([serialize_cliente(cliente) for cliente in clientes], 200)


@clientes_bp.get("/<int:cliente_id>")
def get_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    return success_response(serialize_cliente(cliente), 200)


@clientes_bp.post("")
def create_cliente():
    data = request.get_json() or {}
    cliente = ClienteController.create_cliente(data)

    return success_response(serialize_cliente(cliente), 201)


@clientes_bp.put("/<int:cliente_id>")
def update_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    data = request.get_json() or {}
    updated_cliente = ClienteController.update_cliente(cliente, data)

    return success_response(serialize_cliente(updated_cliente), 200)


@clientes_bp.delete("/<int:cliente_id>")
def delete_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    ClienteController.delete_cliente(cliente)
    return message_response("Cliente eliminado correctamente", 200)
