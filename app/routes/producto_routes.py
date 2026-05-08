from flask import Blueprint, request

from app.api.responses import error_response, message_response, success_response
from app.controllers import ProductoController

"""
Rutas de Productos

Endpoints:
- GET  /api/v1/productos                 -> Lista productos.
- GET  /api/v1/productos/<producto_id>   -> Obtiene un producto por id.
- POST /api/v1/productos                 -> Crea producto. Body JSON ejemplo: {"nombre":"X","precio":"10.00","stock":5}
- PUT  /api/v1/productos/<producto_id>   -> Actualiza producto.
- DELETE /api/v1/productos/<producto_id>-> Elimina producto.

Uso: `ProductoController` contiene la lógica; los precios se serializan como strings para preservar precisión decimal.
"""

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
    """GET /api/v1/productos - Lista productos.

    Response: 200 + lista de productos.
    """
    productos = ProductoController.list_productos()
    return success_response([serialize_producto(producto) for producto in productos], 200)


@productos_bp.get("/<int:producto_id>")
def get_producto(producto_id: int):
    """GET /api/v1/productos/<id> - Obtener producto por id.

    Response: 200 + producto | 404 si no existe.
    """
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return error_response("Producto no encontrado", 404)

    return success_response(serialize_producto(producto), 200)


@productos_bp.post("")
def create_producto():
    """POST /api/v1/productos - Crear producto.

    Body JSON: campos del producto. Response: 201 + producto creado.
    """
    data = request.get_json() or {}
    producto = ProductoController.create_producto(data)

    return success_response(serialize_producto(producto), 201)


@productos_bp.put("/<int:producto_id>")
def update_producto(producto_id: int):
    """PUT /api/v1/productos/<id> - Actualizar producto.

    Body JSON: campos a actualizar. Response: 200 + producto actualizado.
    """
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return error_response("Producto no encontrado", 404)

    data = request.get_json() or {}
    updated_producto = ProductoController.update_producto(producto, data)

    return success_response(serialize_producto(updated_producto), 200)


@productos_bp.delete("/<int:producto_id>")
def delete_producto(producto_id: int):
    """DELETE /api/v1/productos/<id> - Eliminar producto.

    Response: 200 + mensaje de confirmación.
    """
    producto = ProductoController.get_producto(producto_id)
    if producto is None:
        return error_response("Producto no encontrado", 404)

    ProductoController.delete_producto(producto)
    return message_response("Producto eliminado correctamente", 200)
