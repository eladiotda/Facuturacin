from flask import Blueprint, jsonify, request

from app.controllers import ClienteController, ConflictError, ValidationError


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
    return jsonify([serialize_cliente(cliente) for cliente in clientes]), 200


@clientes_bp.get("/<int:cliente_id>")
def get_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(serialize_cliente(cliente)), 200


@clientes_bp.post("")
def create_cliente():
    data = request.get_json(silent=True) or {}
    try:
        cliente = ClienteController.create_cliente(data)
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    except ConflictError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(serialize_cliente(cliente)), 201


@clientes_bp.put("/<int:cliente_id>")
def update_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json(silent=True) or {}
    try:
        updated_cliente = ClienteController.update_cliente(cliente, data)
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    except ConflictError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(serialize_cliente(updated_cliente)), 200


@clientes_bp.delete("/<int:cliente_id>")
def delete_cliente(cliente_id: int):
    cliente = ClienteController.get_cliente(cliente_id)
    if cliente is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    ClienteController.delete_cliente(cliente)
    return jsonify({"message": "Cliente eliminado correctamente"}), 200
