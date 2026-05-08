import { useEffect, useState } from 'react'
import { getFacturas, createFactura } from '../api/facturas'
import { getClientes, createCliente } from '../api/clientes'
import { getProductos, createProducto } from '../api/productos'
import Modal from '../components/ui/Modal'

// ── Modal rápido para crear cliente sin salir de la factura ──────────────────
function QuickClienteModal({ onCreated, onClose }) {
  const [form, setForm] = useState({ nombre: '', correo: '', telefono: '', direccion: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError(null)
    try { const c = await createCliente(form); onCreated(c) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <Modal title="Nuevo cliente rápido" onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-3">
        {error && <p className="text-red-500 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>}
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Nombre *</label>
          <input value={form.nombre} onChange={set('nombre')} required className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Correo *</label>
          <input type="email" value={form.correo} onChange={set('correo')} required className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Teléfono</label>
          <input value={form.telefono} onChange={set('telefono')} className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div className="flex justify-end gap-2 pt-1">
          <button type="button" onClick={onClose} className="px-4 py-2 text-sm rounded-lg border border-gray-200 hover:bg-gray-50">Cancelar</button>
          <button type="submit" disabled={loading} className="px-4 py-2 text-sm rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50">{loading ? 'Guardando…' : 'Guardar'}</button>
        </div>
      </form>
    </Modal>
  )
}

// ── Modal rápido para crear producto sin salir de la factura ─────────────────
function QuickProductoModal({ onCreated, onClose }) {
  const [form, setForm] = useState({ nombre: '', precio: '', stock: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError(null)
    try { const p = await createProducto(form); onCreated(p) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <Modal title="Nuevo producto rápido" onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-3">
        {error && <p className="text-red-500 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>}
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Nombre *</label>
          <input value={form.nombre} onChange={set('nombre')} required className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">Precio *</label>
            <input type="number" min="0" step="0.01" value={form.precio} onChange={set('precio')} required className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">Stock *</label>
            <input type="number" min="0" step="1" value={form.stock} onChange={set('stock')} required className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        <div className="flex justify-end gap-2 pt-1">
          <button type="button" onClick={onClose} className="px-4 py-2 text-sm rounded-lg border border-gray-200 hover:bg-gray-50">Cancelar</button>
          <button type="submit" disabled={loading} className="px-4 py-2 text-sm rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50">{loading ? 'Guardando…' : 'Guardar'}</button>
        </div>
      </form>
    </Modal>
  )
}

// ── Formulario nueva factura ─────────────────────────────────────────────────
function NuevaFacturaForm({ clientes, productos, onSaved, onCancel, onNuevoCliente, onNuevoProducto }) {
  const [numero, setNumero]       = useState('')
  const [clienteId, setClienteId] = useState('')
  const [lineas, setLineas]       = useState([{ producto_id: '', cantidad: 1, precio_unitario: '' }])
  const [saving, setSaving]       = useState(false)
  const [error, setError]         = useState(null)

  const addLinea = () => setLineas(l => [...l, { producto_id: '', cantidad: 1, precio_unitario: '' }])
  const removeLinea = (i) => setLineas(l => l.filter((_, idx) => idx !== i))
  const setLinea = (i, k, v) => setLineas(l => l.map((x, idx) => idx === i ? { ...x, [k]: v } : x))

  const onProductoChange = (i, pid) => {
    const p = productos.find(p => String(p.id) === String(pid))
    setLinea(i, 'producto_id', pid)
    if (p) setLinea(i, 'precio_unitario', p.precio)
  }

  const total = lineas.reduce((s, l) => {
    const sub = parseFloat(l.precio_unitario || 0) * parseInt(l.cantidad || 0)
    return s + (isNaN(sub) ? 0 : sub)
  }, 0)

  const handleSubmit = async (e) => {
    e.preventDefault(); setSaving(true); setError(null)
    try {
      await createFactura({
        numero,
        cliente_id: parseInt(clienteId),
        detalles: lineas.map(l => ({
          producto_id: parseInt(l.producto_id),
          cantidad: parseInt(l.cantidad),
          precio_unitario: l.precio_unitario,
        })),
      })
      onSaved()
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <p className="text-red-500 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>}

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Número de factura *</label>
          <input value={numero} onChange={e => setNumero(e.target.value)} required placeholder="FAC-001"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <div className="flex items-center justify-between mb-1">
            <label className="text-xs font-medium text-gray-500">Cliente *</label>
            <button type="button" onClick={onNuevoCliente}
              className="text-xs text-blue-600 hover:underline">+ Nuevo</button>
          </div>
          <select value={clienteId} onChange={e => setClienteId(e.target.value)} required
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
            <option value="">Seleccionar cliente…</option>
            {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
          </select>
        </div>
      </div>

      {/* Líneas de detalle */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-gray-500">Productos</span>
          <button type="button" onClick={onNuevoProducto}
            className="text-xs text-blue-600 hover:underline">+ Nuevo producto</button>
        </div>

        <div className="space-y-2">
          {lineas.map((l, i) => (
            <div key={i} className="grid grid-cols-12 gap-2 items-center">
              <div className="col-span-5">
                <select value={l.producto_id} onChange={e => onProductoChange(i, e.target.value)} required
                  className="w-full border border-gray-200 rounded-lg px-2 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
                  <option value="">Producto…</option>
                  {productos.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
                </select>
              </div>
              <div className="col-span-2">
                <input type="number" min="1" value={l.cantidad}
                  onChange={e => setLinea(i, 'cantidad', e.target.value)} required
                  placeholder="Cant."
                  className="w-full border border-gray-200 rounded-lg px-2 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div className="col-span-3">
                <input type="number" min="0" step="0.01" value={l.precio_unitario}
                  onChange={e => setLinea(i, 'precio_unitario', e.target.value)} required
                  placeholder="Precio"
                  className="w-full border border-gray-200 rounded-lg px-2 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div className="col-span-2 text-right">
                <span className="text-xs text-gray-500 mr-1">
                  ${(parseFloat(l.precio_unitario || 0) * parseInt(l.cantidad || 0) || 0).toFixed(2)}
                </span>
                {lineas.length > 1 && (
                  <button type="button" onClick={() => removeLinea(i)}
                    className="text-red-400 hover:text-red-600 text-lg leading-none">&times;</button>
                )}
              </div>
            </div>
          ))}
        </div>

        <button type="button" onClick={addLinea}
          className="mt-2 text-xs text-blue-600 hover:underline">+ Agregar línea</button>
      </div>

      {/* Total */}
      <div className="flex justify-end border-t border-gray-100 pt-3">
        <span className="text-sm font-semibold text-gray-700">Total: ${total.toFixed(2)}</span>
      </div>

      <div className="flex justify-end gap-2">
        <button type="button" onClick={onCancel}
          className="px-4 py-2 text-sm rounded-lg border border-gray-200 hover:bg-gray-50">
          Cancelar
        </button>
        <button type="submit" disabled={saving}
          className="px-4 py-2 text-sm rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50">
          {saving ? 'Guardando…' : 'Crear factura'}
        </button>
      </div>
    </form>
  )
}

// ── Página principal Facturas ────────────────────────────────────────────────
export default function Facturas() {
  const [facturas, setFacturas]   = useState([])
  const [clientes, setClientes]   = useState([])
  const [productos, setProductos] = useState([])
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)

  const [showForm, setShowForm]             = useState(false)
  const [showQuickCliente, setShowQuickCliente] = useState(false)
  const [showQuickProducto, setShowQuickProducto] = useState(false)

  const [detalle, setDetalle] = useState(null)

  const loadAll = () => {
    setLoading(true)
    Promise.all([getFacturas(), getClientes(), getProductos()])
      .then(([f, c, p]) => { setFacturas(f); setClientes(c); setProductos(p) })
      .catch(() => setError('No se pudieron cargar los datos'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { loadAll() }, [])

  const handleSaved = () => { setShowForm(false); loadAll() }

  const handleQuickClienteCreated = (c) => {
    setClientes(prev => [...prev, c])
    setShowQuickCliente(false)
  }

  const handleQuickProductoCreated = (p) => {
    setProductos(prev => [...prev, p])
    setShowQuickProducto(false)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-700">Facturas</h1>
        {!showForm && (
          <button onClick={() => setShowForm(true)}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            + Nueva factura
          </button>
        )}
      </div>

      {/* Formulario nueva factura (inline, no modal) */}
      {showForm && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <h2 className="text-sm font-semibold text-gray-600 mb-4">Nueva factura</h2>
          <NuevaFacturaForm
            clientes={clientes}
            productos={productos}
            onSaved={handleSaved}
            onCancel={() => setShowForm(false)}
            onNuevoCliente={() => setShowQuickCliente(true)}
            onNuevoProducto={() => setShowQuickProducto(true)}
          />
        </div>
      )}

      {/* Lista de facturas */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        {loading && <p className="text-sm text-gray-400 p-5">Cargando...</p>}
        {error   && <p className="text-sm text-red-500 p-5">{error}</p>}
        {!loading && !error && facturas.length === 0 && (
          <p className="text-sm text-gray-400 p-5">No hay facturas registradas.</p>
        )}
        {!loading && facturas.length > 0 && (
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr className="text-left text-gray-500 text-xs uppercase tracking-wide">
                <th className="px-4 py-3 font-medium">Número</th>
                <th className="px-4 py-3 font-medium">Cliente</th>
                <th className="px-4 py-3 font-medium">Fecha</th>
                <th className="px-4 py-3 font-medium text-right">Total</th>
                <th className="px-4 py-3 font-medium text-right">Detalle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {facturas.map(f => (
                <tr key={f.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-blue-600">{f.numero}</td>
                  <td className="px-4 py-3 text-gray-600">{f.cliente?.nombre ?? '—'}</td>
                  <td className="px-4 py-3 text-gray-400">
                    {new Date(f.fecha_emision).toLocaleDateString('es-CO')}
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-gray-700">
                    ${parseFloat(f.total).toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => setDetalle(f)}
                      className="text-xs px-3 py-1 rounded-lg border border-gray-200 hover:bg-gray-100 text-gray-600">
                      Ver
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal detalle de factura */}
      {detalle && (
        <Modal title={`Factura ${detalle.numero}`} onClose={() => setDetalle(null)}>
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2 text-gray-600">
              <div><span className="text-gray-400 text-xs block">Cliente</span>{detalle.cliente?.nombre ?? '—'}</div>
              <div><span className="text-gray-400 text-xs block">Fecha</span>{new Date(detalle.fecha_emision).toLocaleDateString('es-CO')}</div>
            </div>
            <table className="w-full mt-2">
              <thead>
                <tr className="text-left text-gray-400 text-xs border-b border-gray-100">
                  <th className="pb-1 font-medium">Producto</th>
                  <th className="pb-1 font-medium text-center">Cant.</th>
                  <th className="pb-1 font-medium text-right">P. Unit.</th>
                  <th className="pb-1 font-medium text-right">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {(detalle.detalles || []).map((d, i) => (
                  <tr key={i} className="border-b border-gray-50">
                    <td className="py-1 text-gray-700">{d.producto?.nombre ?? `#${d.producto_id}`}</td>
                    <td className="py-1 text-center text-gray-500">{d.cantidad}</td>
                    <td className="py-1 text-right text-gray-500">${parseFloat(d.precio_unitario).toFixed(2)}</td>
                    <td className="py-1 text-right font-medium text-gray-700">${parseFloat(d.subtotal).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="flex justify-end pt-1 font-semibold text-gray-800">
              Total: ${parseFloat(detalle.total).toFixed(2)}
            </div>
          </div>
        </Modal>
      )}

      {/* Modales rápidos */}
      {showQuickCliente  && <QuickClienteModal  onCreated={handleQuickClienteCreated}  onClose={() => setShowQuickCliente(false)} />}
      {showQuickProducto && <QuickProductoModal onCreated={handleQuickProductoCreated} onClose={() => setShowQuickProducto(false)} />}
    </div>
  )
}
