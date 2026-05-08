const BASE = '/api/v1/facturas'

export async function getFacturas() {
  const res = await fetch(BASE)
  if (!res.ok) throw new Error('Error al obtener facturas')
  const json = await res.json()
  return json.data
}

export async function getFactura(id) {
  const res = await fetch(`${BASE}/${id}`)
  if (!res.ok) throw new Error('Factura no encontrada')
  const json = await res.json()
  return json.data
}

export async function createFactura(body) {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Error al crear factura')
  return json.data
}
