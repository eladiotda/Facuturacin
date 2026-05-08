const BASE = '/api/v1/productos'

export async function getProductos() {
  const res = await fetch(BASE)
  if (!res.ok) throw new Error('Error al obtener productos')
  const json = await res.json()
  return json.data
}

export async function getProducto(id) {
  const res = await fetch(`${BASE}/${id}`)
  if (!res.ok) throw new Error('Producto no encontrado')
  const json = await res.json()
  return json.data
}

export async function createProducto(body) {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al crear producto')
  return json.data
}

export async function updateProducto(id, body) {
  const res = await fetch(`${BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al actualizar producto')
  return json.data
}

export async function deleteProducto(id) {
  const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al eliminar producto')
  return json
}
