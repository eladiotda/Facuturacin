import pytest

from app.controllers import ConflictError, ProductoController, ValidationError


def test_create_and_get_producto(app_context):
    created_producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": "15000.50", "stock": 12}
    )

    found_producto = ProductoController.get_producto(created_producto.id)

    assert found_producto is not None
    assert found_producto.nombre == "Arroz"
    assert str(found_producto.precio) == "15000.50"


def test_list_productos_returns_created_records(app_context):
    ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )
    ProductoController.create_producto(
        {"nombre": "Aceite", "precio": 20000, "stock": 3}
    )

    productos = ProductoController.list_productos()

    assert len(productos) == 2
    assert productos[0].nombre == "Arroz"
    assert productos[1].nombre == "Aceite"


def test_update_producto_persists_changes(app_context):
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )

    updated_producto = ProductoController.update_producto(
        producto,
        {"precio": "12500.75", "stock": 9},
    )

    assert str(updated_producto.precio) == "12500.75"
    assert updated_producto.stock == 9


def test_delete_producto_removes_record(app_context):
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )

    ProductoController.delete_producto(producto)

    assert ProductoController.get_producto(producto.id) is None


def test_create_producto_requires_required_fields(app_context):
    with pytest.raises(ValidationError):
        ProductoController.create_producto({"nombre": "   "})


def test_create_producto_rejects_duplicate_nombre(app_context):
    ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )

    with pytest.raises(ConflictError):
        ProductoController.create_producto(
            {"nombre": "Arroz", "precio": 12000, "stock": 8}
        )


def test_create_producto_rejects_negative_values(app_context):
    with pytest.raises(ValidationError):
        ProductoController.create_producto(
            {"nombre": "Arroz", "precio": -100, "stock": 1}
        )

    with pytest.raises(ValidationError):
        ProductoController.create_producto(
            {"nombre": "Aceite", "precio": 100, "stock": -1}
        )


def test_update_producto_rejects_empty_nombre(app_context):
    producto = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )

    with pytest.raises(ValidationError):
        ProductoController.update_producto(producto, {"nombre": "   "})


def test_update_producto_rejects_duplicate_nombre(app_context):
    producto_1 = ProductoController.create_producto(
        {"nombre": "Arroz", "precio": 10000, "stock": 5}
    )
    ProductoController.create_producto(
        {"nombre": "Aceite", "precio": 20000, "stock": 3}
    )

    with pytest.raises(ConflictError):
        ProductoController.update_producto(producto_1, {"nombre": "Aceite"})
