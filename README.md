Facturacion API — Endpoints y ejemplos curl
=========================================

Base URL: http://127.0.0.1:5000

Formato general de respuestas:
- `success_response(data, status)` devuelve JSON `{ "data": ..., "status": ... }` (ver código fuente)
- `error_response(msg, status)` devuelve `{ "error": msg }`

Clientes
--------
- Lista clientes

```bash
curl -s http://127.0.0.1:5000/api/v1/clientes
```

- Obtener cliente por id

```bash
curl -s http://127.0.0.1:5000/api/v1/clientes/1
```

- Crear cliente

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","correo":"juan@example.com","telefono":"3001234567","direccion":"Calle 1"}' \
  http://127.0.0.1:5000/api/v1/clientes
```

- Actualizar cliente

```bash
curl -s -X PUT -H "Content-Type: application/json" \
  -d '{"telefono":"3107654321"}' \
  http://127.0.0.1:5000/api/v1/clientes/1
```

- Eliminar cliente

```bash
curl -s -X DELETE http://127.0.0.1:5000/api/v1/clientes/1
```

Productos
---------
- Lista productos

```bash
curl -s http://127.0.0.1:5000/api/v1/productos
```

- Obtener producto

```bash
curl -s http://127.0.0.1:5000/api/v1/productos/1
```

- Crear producto

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"nombre":"Galleta","precio":"1.50","stock":100}' \
  http://127.0.0.1:5000/api/v1/productos
```

- Actualizar producto

```bash
curl -s -X PUT -H "Content-Type: application/json" \
  -d '{"stock":90}' \
  http://127.0.0.1:5000/api/v1/productos/1
```

- Eliminar producto

```bash
curl -s -X DELETE http://127.0.0.1:5000/api/v1/productos/1
```

Facturas
--------
- Lista facturas

```bash
curl -s http://127.0.0.1:5000/api/v1/facturas
```

- Obtener factura

```bash
curl -s http://127.0.0.1:5000/api/v1/facturas/1
```

- Crear factura

Body ejemplo:

```json
{
  "cliente_id": 1,
  "detalles": [
    {"producto_id": 2, "cantidad": 3, "precio_unitario": "10.00"},
    {"producto_id": 5, "cantidad": 1, "precio_unitario": "25.00"}
  ]
}
```

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d @factura.json \
  http://127.0.0.1:5000/api/v1/facturas
```

Notas
-----
- Las rutas están bajo `/api/v1/`.
- Si la app retorna `{"error":"Recurso no encontrado"}` en `/` usa cualquiera de los endpoints anteriores.
- Los precios se serializan como strings para mantener precisión decimal.
- Para pruebas locales asegúrate de tener `.env` configurado con `DB_ENGINE=sqlserver` y credenciales correctas.
