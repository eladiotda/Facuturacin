from flask import Blueprint, request

from app.api.responses import error_response, success_response
from app.controllers import FacturaController


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
    facturas = FacturaController.list_facturas()
    return success_response([serialize_factura(factura) for factura in facturas], 200)


@facturas_bp.get("/<int:factura_id>")
def get_factura(factura_id: int):
    factura = FacturaController.get_factura(factura_id)
    if factura is None:
        return error_response("Factura no encontrada", 404)

    return success_response(serialize_factura(factura), 200)


@facturas_bp.post("")
def create_factura():
    data = request.get_json() or {}
    factura = FacturaController.create_factura(data)

    return success_response(serialize_factura(factura), 201)
