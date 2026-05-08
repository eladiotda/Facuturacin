import pytest

from app.controllers import (
    ClienteController,
    FacturaController,
    NotFoundError,
    ProductoController,
    ValidationError,
)


def test_create_factura_creates_details_and_total(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )
    producto_1 = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "10000.00", "stock": 10}
    )
    producto_2 = ProductoController.create_producto(
        {"nombre": "Aceite", "precio": "15000.50", "stock": 8}
    )

    factura = FacturaController.create_factura(
        {
            "numero": "FAC-001",
            "cliente_id": cliente.id,
            "detalles": [
                {"producto_id": producto_1.id, "cantidad": 2},
                {"producto_id": producto_2.id, "cantidad": 1},
            ],
        }
    )

    assert factura.numero == "FAC-001"
    assert str(factura.total) == "35000.50"
    assert len(factura.detalles) == 2
    assert producto_1.stock == 8
    assert producto_2.stock == 7


def test_create_factura_rejects_missing_cliente(app_context):
    with pytest.raises(NotFoundError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": 999,
                "detalles": [{"producto_id": 1, "cantidad": 1}],
            }
        )


def test_create_factura_rejects_missing_producto(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )

    with pytest.raises(NotFoundError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [{"producto_id": 999, "cantidad": 1}],
            }
        )


def test_create_factura_rejects_insufficient_stock(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "10000.00", "stock": 1}
    )

    with pytest.raises(ValidationError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [{"producto_id": producto.id, "cantidad": 2}],
            }
        )


def test_create_factura_rejects_duplicate_numero(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "10000.00", "stock": 5}
    )

    FacturaController.create_factura(
        {
            "numero": "FAC-001",
            "cliente_id": cliente.id,
            "detalles": [{"producto_id": producto.id, "cantidad": 1}],
        }
    )

    with pytest.raises(ValidationError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [{"producto_id": producto.id, "cantidad": 1}],
            }
        )


def test_create_factura_rejects_empty_detalles(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )

    with pytest.raises(ValidationError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [],
            }
        )


def test_create_factura_rejects_duplicate_producto_in_detalles(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "10000.00", "stock": 5}
    )

    with pytest.raises(ValidationError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [
                    {"producto_id": producto.id, "cantidad": 1},
                    {"producto_id": producto.id, "cantidad": 1},
                ],
            }
        )


def test_create_factura_rejects_invalid_cantidad(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Eladio", "correo": "eladio@example.com"}
    )
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "10000.00", "stock": 5}
    )

    with pytest.raises(ValidationError):
        FacturaController.create_factura(
            {
                "numero": "FAC-001",
                "cliente_id": cliente.id,
                "detalles": [{"producto_id": producto.id, "cantidad": 0}],
            }
        )
