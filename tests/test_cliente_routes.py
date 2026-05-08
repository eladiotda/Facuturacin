def test_list_clientes_returns_empty_list(client):
    response = client.get("/api/v1/clientes")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_cliente_returns_created_resource(client):
    response = client.post(
        "/api/v1/clientes",
        json={
            "nombre": "Eladio Lopez",
            "correo": "eladio@example.com",
            "telefono": "3001234567",
            "direccion": "Calle 1",
        },
    )

    body = response.get_json()

    assert response.status_code == 201
    assert body["nombre"] == "Eladio Lopez"
    assert body["correo"] == "eladio@example.com"


def test_get_cliente_returns_existing_resource(client):
    created_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    )
    cliente_id = created_response.get_json()["id"]

    response = client.get(f"/api/v1/clientes/{cliente_id}")

    assert response.status_code == 200
    assert response.get_json()["nombre"] == "Ana"


def test_update_cliente_returns_updated_resource(client):
    created_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    )
    cliente_id = created_response.get_json()["id"]

    response = client.put(
        f"/api/v1/clientes/{cliente_id}",
        json={"telefono": "3000000000"},
    )

    assert response.status_code == 200
    assert response.get_json()["telefono"] == "3000000000"


def test_delete_cliente_removes_resource(client):
    created_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    )
    cliente_id = created_response.get_json()["id"]

    delete_response = client.delete(f"/api/v1/clientes/{cliente_id}")
    get_response = client.get(f"/api/v1/clientes/{cliente_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Cliente eliminado correctamente"
    assert get_response.status_code == 404


def test_create_cliente_rejects_missing_required_fields(client):
    response = client.post(
        "/api/v1/clientes",
        json={"nombre": "", "correo": ""},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_cliente_rejects_duplicate_correo(client):
    client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    )

    response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana 2", "correo": "ana@example.com"},
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Ya existe un cliente con ese correo"


def test_update_cliente_rejects_invalid_correo(client):
    created_response = client.post(
        "/api/v1/clientes",
        json={"nombre": "Ana", "correo": "ana@example.com"},
    )
    cliente_id = created_response.get_json()["id"]

    response = client.put(
        f"/api/v1/clientes/{cliente_id}",
        json={"correo": "correo-invalido"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "El correo no tiene un formato valido"
