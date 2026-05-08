def test_list_facturas_returns_empty_list(client):
    response = client.get("/api/v1/facturas")

    assert response.status_code == 200
    assert response.get_json() == {"data": []}


def test_create_factura_returns_created_resource(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": "10000.00", "stock": 5},
    )

    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-001",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 2}
            ],
        },
    )

    body = response.get_json()["data"]

    assert response.status_code == 201
    assert body["numero"] == "FAC-001"
    assert body["total"] == "20000.00"
    assert len(body["detalles"]) == 1


def test_get_factura_returns_existing_resource(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Cafe", "precio": "8000.00", "stock": 4},
    )
    factura_response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-002",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 1}
            ],
        },
    )
    factura_id = factura_response.get_json()["data"]["id"]

    response = client.get(f"/api/v1/facturas/{factura_id}")

    assert response.status_code == 200
    assert response.get_json()["data"]["numero"] == "FAC-002"


def test_create_factura_rejects_missing_cliente(client):
    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-001",
            "cliente_id": 999,
            "detalles": [{"producto_id": 1, "cantidad": 1}],
        },
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "El cliente con id 999 no existe"


def test_create_factura_rejects_insufficient_stock(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Aceite", "precio": "15000.00", "stock": 1},
    )

    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-003",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 2}
            ],
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Stock insuficiente para el producto Aceite"


def test_create_factura_rejects_duplicate_numero(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": "10000.00", "stock": 5},
    )

    client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-001",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 1}
            ],
        },
    )

    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-001",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 1}
            ],
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Ya existe una factura con ese numero"


def test_create_factura_rejects_duplicate_producto_in_detalles(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": "10000.00", "stock": 5},
    )

    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-010",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 1},
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 1},
            ],
        },
    )

    assert response.status_code == 400
    assert (
        response.get_json()["error"]
        == f"El producto con id {producto_response.get_json()['data']['id']} no puede repetirse en la factura"
    )


def test_create_factura_rejects_invalid_cantidad(client):
    cliente_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Eladio", "correo": "eladio@example.com"},
    )
    producto_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Cafe", "precio": "8000.00", "stock": 4},
    )

    response = client.post(
        "/api/v1/facturas",
        json={
            "numero": "FAC-011",
            "cliente_id": cliente_response.get_json()["data"]["id"],
            "detalles": [
                {"producto_id": producto_response.get_json()["data"]["id"], "cantidad": 0}
            ],
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "La cantidad debe ser mayor que cero"


def test_create_factura_rejects_invalid_json_payload(client):
    response = client.post(
        "/api/v1/facturas",
        data="{invalid-json}",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Solicitud invalida"
