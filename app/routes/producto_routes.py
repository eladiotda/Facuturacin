from flask import Blueprint, jsonify, request

from app.controllers import ConflictError, ProductoController, ValidationError


productos_bp = Blueprint("productos", __name__, url_prefix="/api/v1/productos")


def serialize_producto(producto) -> dict:
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": str(producto.precio),
        "stock": producto.stock,
        "created_at": producto.created_at.isoformat(),
        "updated_at": producto.updated_at.isoformat(),
    }


@productos_bp.get("")
def list_productos():
    productos = ProductoController.list_productos()
    return jsonify([serialize_producto(producto) for producto in productos]), 200


@productos_bp.get("/<int:producto_id>")
def get_producto(producto_id: int):
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify(serialize_producto(producto)), 200


@productos_bp.post("")
def create_producto():
    data = request.get_json(silent=True) or {}
    try:
        producto = ProductoController.create_producto(data)
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    except ConflictError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(serialize_producto(producto)), 201


@productos_bp.put("/<int:producto_id>")
def update_producto(producto_id: int):
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json(silent=True) or {}
    try:
        updated_producto = ProductoController.update_producto(producto, data)
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    except ConflictError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(serialize_producto(updated_producto)), 200


@productos_bp.delete("/<int:producto_id>")
def delete_producto(producto_id: int):
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    ProductoController.delete_producto(producto)
    return jsonify({"message": "Producto eliminado correctamente"}), 200
