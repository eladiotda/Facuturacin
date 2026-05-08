from flask import Blueprint, request

from app.api.responses import error_response, message_response, success_response
from app.controllers import ClienteController

"""
Rutas de Clientes

Endpoints:
- GET  /api/v1/clientes                 -> Lista todos los clientes.
- GET  /api/v1/clientes/<cliente_id>    -> Obtiene un cliente por id.
- POST /api/v1/clientes                 -> Crea un nuevo cliente. JSON body ejemplo:
    {"nombre": "Juan", "correo": "a@b.com", "telefono": "123", "direccion": "..."}
- PUT  /api/v1/clientes/<cliente_id>    -> Actualiza un cliente existente. Envía los campos a actualizar en JSON.
- DELETE /api/v1/clientes/<cliente_id> -> Elimina un cliente.

Respuestas (uso general):
- `success_response(data, status)` devuelve JSON con `data` y código HTTP.
- `error_response(msg, status)` devuelve error con mensaje y código.
- `message_response(msg, status)` devuelve mensaje simple.

Uso: estas rutas usan `ClienteController` para la lógica de negocio y devuelven datos serializados.
"""


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
    """GET /api/v1/clientes - Lista clientes.

    Response: 200 + lista de clientes.
    """
    clientes = ClienteController.list_clientes()
    return success_response([serialize_cliente(cliente) for cliente in clientes], 200)


@clientes_bp.get("/<int:cliente_id>")
def get_cliente(cliente_id: int):
    """GET /api/v1/clientes/<id> - Obtener cliente por id.

    Response: 200 + cliente | 404 si no existe.
    """
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    return success_response(serialize_cliente(cliente), 200)


@clientes_bp.post("")
def create_cliente():
    """POST /api/v1/clientes - Crear cliente.

    Body JSON: campos del cliente. Response: 201 + cliente creado.
    """
    data = request.get_json() or {}
    cliente = ClienteController.create_cliente(data)

    return success_response(serialize_cliente(cliente), 201)


@clientes_bp.put("/<int:cliente_id>")
def update_cliente(cliente_id: int):
    """PUT /api/v1/clientes/<id> - Actualizar cliente.

    Body JSON: campos a actualizar. Response: 200 + cliente actualizado.
    """
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    data = request.get_json() or {}
    updated_cliente = ClienteController.update_cliente(cliente, data)

    return success_response(serialize_cliente(updated_cliente), 200)


@clientes_bp.delete("/<int:cliente_id>")
def delete_cliente(cliente_id: int):
    """DELETE /api/v1/clientes/<id> - Eliminar cliente.

    Response: 200 + mensaje de confirmación.
    """
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return error_response("Cliente no encontrado", 404)

    ClienteController.delete_cliente(cliente)
    return message_response("Cliente eliminado correctamente", 200)
