def test_list_productos_returns_empty_list(client):
    response = client.get("/api/v1/productos")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_producto_returns_created_resource(client):
    response = client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": "12500.50", "stock": 10},
    )

    body = response.get_json()

    assert response.status_code == 201
    assert body["nombre"] == "Arroz"
    assert body["precio"] == "12500.50"


def test_get_producto_returns_existing_resource(client):
    created_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Aceite", "precio": 22000, "stock": 6},
    )
    producto_id = created_response.get_json()["id"]

    response = client.get(f"/api/v1/productos/{producto_id}")

    assert response.status_code == 200
    assert response.get_json()["nombre"] == "Aceite"


def test_update_producto_returns_updated_resource(client):
    created_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Azucar", "precio": 4000, "stock": 8},
    )
    producto_id = created_response.get_json()["id"]

    response = client.put(
        f"/api/v1/productos/{producto_id}",
        json={"precio": "4500.75", "stock": 9},
    )

    assert response.status_code == 200
    assert response.get_json()["precio"] == "4500.75"
    assert response.get_json()["stock"] == 9


def test_delete_producto_removes_resource(client):
    created_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Cafe", "precio": 9500, "stock": 4},
    )
    producto_id = created_response.get_json()["id"]

    delete_response = client.delete(f"/api/v1/productos/{producto_id}")
    get_response = client.get(f"/api/v1/productos/{producto_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Producto eliminado correctamente"
    assert get_response.status_code == 404


def test_create_producto_rejects_missing_required_fields(client):
    response = client.post(
        "/api/v1/productos",
        json={"nombre": "", "precio": "", "stock": ""},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_producto_rejects_duplicate_nombre(client):
    client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": 12000, "stock": 5},
    )

    response = client.post(
        "/api/v1/productos",
        json={"nombre": "Arroz", "precio": 13000, "stock": 7},
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Ya existe un producto con ese nombre"


def test_update_producto_rejects_invalid_precio(client):
    created_response = client.post(
        "/api/v1/productos",
        json={"nombre": "Harina", "precio": 3000, "stock": 11},
    )
    producto_id = created_response.get_json()["id"]

    response = client.put(
        f"/api/v1/productos/{producto_id}",
        json={"precio": -10},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "El precio no puede ser negativo"
