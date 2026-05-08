from flask import Blueprint, request

from app.api.responses import error_response, success_response
from app.controllers import FacturaController


"""
Rutas de Facturas

Endpoints:
- GET  /api/v1/facturas              -> Lista todas las facturas.
- GET  /api/v1/facturas/<factura_id> -> Obtiene una factura por id.
- POST /api/v1/facturas              -> Crea una factura. Body JSON esperado:
     {
         "cliente_id": 1,
         "detalles": [{"producto_id": 2, "cantidad": 3, "precio_unitario": "10.00"}, ...]
     }

Respuestas:
- 200 con datos (lista o elemento), 201 en creación, 404 si no existe.

Uso: `FacturaController` gestiona la lógica y validaciones; la serialización incluye cliente y detalles.
"""

facturas_bp = Blueprint("facturas", __name__, url_prefix="/api/v1/facturas")


def serialize_factura(factura) -> dict:
    return {
        "id": factura.id,
        "numero": factura.numero,
        "fecha_emision": factura.fecha_emision.isoformat(),
        "cliente": {
            "id": factura.cliente.id,
            "nombre": factura.cliente.nombre,
            "correo": factura.cliente.correo,
        },
        "total": str(factura.total),
        "detalles": [
            {
                "id": detalle.id,
                "producto": {
                    "id": detalle.producto.id,
                    "nombre": detalle.producto.nombre,
                },
                "cantidad": detalle.cantidad,
                "precio_unitario": str(detalle.precio_unitario),
                "subtotal": str(detalle.subtotal),
            }
            for detalle in factura.detalles
        ],
        "created_at": factura.created_at.isoformat(),
        "updated_at": factura.updated_at.isoformat(),
    }


@facturas_bp.get("")
def list_facturas():
    """GET /api/v1/facturas - Lista facturas.

    Response: 200 + lista de facturas serializadas.
    """
    facturas = FacturaController.list_facturas()
    return success_response([serialize_factura(factura) for factura in facturas], 200)


@facturas_bp.get("/<int:factura_id>")
def get_factura(factura_id: int):
    """GET /api/v1/facturas/<id> - Obtener factura por id.

    Response: 200 + factura o 404 si no existe.
    """
    factura = FacturaController.get_factura(factura_id)
    if factura is None:
        return error_response("Factura no encontrada", 404)

    return success_response(serialize_factura(factura), 200)


@facturas_bp.post("")
def create_factura():
    """POST /api/v1/facturas - Crear factura.

    Body JSON: debe incluir `cliente_id` y `detalles`.
    Response: 201 + factura creada.
    """
    data = request.get_json() or {}
    factura = FacturaController.create_factura(data)

    return success_response(serialize_factura(factura), 201)
