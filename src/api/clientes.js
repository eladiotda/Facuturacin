const BASE = '/api/v1/clientes'

export async function getClientes() {
  const res = await fetch(BASE)
  if (!res.ok) throw new Error('Error al obtener clientes')
  const json = await res.json()
  return json.data
}

export async function getCliente(id) {
  const res = await fetch(`${BASE}/${id}`)
  if (!res.ok) throw new Error('Cliente no encontrado')
  const json = await res.json()
  return json.data
}

export async function createCliente(body) {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al crear cliente')
  return json.data
}

export async function updateCliente(id, body) {
  const res = await fetch(`${BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al actualizar cliente')
  return json.data
}

export async function deleteCliente(id) {
  const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al eliminar cliente')
  return json
}
