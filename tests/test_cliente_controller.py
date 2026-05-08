from app.controllers import ClienteController


def test_create_and_get_cliente(app_context):
    created_cliente = ClienteController.create_cliente(
        {
            "nombre": "Eladio Lopez",
            "correo": "eladio@example.com",
            "telefono": "3001234567",
            "direccion": "Calle 1",
        }
    )

    found_cliente = ClienteController.get_cliente(created_cliente.id)

    assert found_cliente is not None
    assert found_cliente.nombre == "Eladio Lopez"
    assert found_cliente.correo == "eladio@example.com"


def test_list_clientes_returns_created_records(app_context):
    ClienteController.create_cliente(
        {"nombre": "Ana", "correo": "ana@example.com"}
    )
    ClienteController.create_cliente(
        {"nombre": "Luis", "correo": "luis@example.com"}
    )

    clientes = ClienteController.list_clientes()

    assert len(clientes) == 2
    assert clientes[0].nombre == "Ana"
    assert clientes[1].nombre == "Luis"


def test_update_cliente_persists_changes(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Ana", "correo": "ana@example.com"}
    )

    updated_cliente = ClienteController.update_cliente(
        cliente,
        {"telefono": "3000000000", "direccion": "Carrera 10"},
    )

    assert updated_cliente.telefono == "3000000000"
    assert updated_cliente.direccion == "Carrera 10"


def test_delete_cliente_removes_record(app_context):
    cliente = ClienteController.create_cliente(
        {"nombre": "Ana", "correo": "ana@example.com"}
    )

    ClienteController.delete_cliente(cliente)

    assert ClienteController.get_cliente(cliente.id) is None
