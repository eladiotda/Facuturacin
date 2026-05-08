import { useEffect, useState } from 'react'
import { getProductos, createProducto, updateProducto, deleteProducto } from '../api/productos'
import Modal from '../components/ui/Modal'
import ConfirmDialog from '../components/ui/ConfirmDialog'

const EMPTY = { nombre: '', precio: '', stock: '' }

function ProductoForm({ initial, onSave, onCancel, loading, error }) {
  const [form, setForm] = useState(initial)
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave(form) }} className="space-y-3">
      {error && <p className="text-red-500 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>}
      <div>
        <label className="text-xs font-medium text-gray-500 block mb-1">Nombre *</label>
        <input value={form.nombre} onChange={set('nombre')} required
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Precio *</label>
          <input type="number" min="0" step="0.01" value={form.precio} onChange={set('precio')} required
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="text-xs font-medium text-gray-500 block mb-1">Stock *</label>
          <input type="number" min="0" step="1" value={form.stock} onChange={set('stock')} required
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <button type="button" onClick={onCancel}
          className="px-4 py-2 text-sm rounded-lg border border-gray-200 hover:bg-gray-50">
          Cancelar
        </button>
        <button type="submit" disabled={loading}
          className="px-4 py-2 text-sm rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50">
          {loading ? 'Guardando…' : 'Guardar'}
        </button>
      </div>
    </form>
  )
}

function StockBadge({ stock }) {
  if (stock === 0)  return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-red-100 text-red-600">Sin stock</span>
  if (stock <= 2)   return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-700">x{stock} bajo</span>
  return <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-700">x{stock}</span>
}

export default function Productos() {
  const [productos, setProductos] = useState([])
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)
  const [modal, setModal]         = useState(null)
  const [saving, setSaving]       = useState(false)
  const [saveError, setSaveError] = useState(null)
  const [toDelete, setToDelete]   = useState(null)

  const load = () => {
    setLoading(true)
    getProductos()
      .then(setProductos)
      .catch(() => setError('No se pudieron cargar los productos'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    setLoading(true)
    getProductos()
      .then(setProductos)
      .catch(() => setError('No se pudieron cargar los productos'))
      .finally(() => setLoading(false))
  }, [])

  const openCreate = () => { setSaveError(null); setModal({ mode: 'create', data: EMPTY }) }
  const openEdit   = (p) => { setSaveError(null); setModal({ mode: 'edit', data: { nombre: p.nombre, precio: p.precio, stock: p.stock }, id: p.id }) }
  const closeModal = () => setModal(null)

  const handleSave = async (form) => {
    setSaving(true); setSaveError(null)
    try {
      if (modal.mode === 'create') await createProducto(form)
      else await updateProducto(modal.id, form)
      closeModal(); load()
    } catch (e) {
      setSaveError(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    try {
      await deleteProducto(toDelete.id)
      setToDelete(null); load()
    } catch (e) {
      alert(e.message)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-700">Productos</h1>
        <button onClick={openCreate}
          className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          + Nuevo producto
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        {loading && <p className="text-sm text-gray-400 p-5">Cargando...</p>}
        {error   && <p className="text-sm text-red-500 p-5">{error}</p>}
        {!loading && !error && productos.length === 0 && (
          <p className="text-sm text-gray-400 p-5">No hay productos registrados.</p>
        )}
        {!loading && productos.length > 0 && (
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr className="text-left text-gray-500 text-xs uppercase tracking-wide">
                <th className="px-4 py-3 font-medium">Nombre</th>
                <th className="px-4 py-3 font-medium">Precio</th>
                <th className="px-4 py-3 font-medium">Stock</th>
                <th className="px-4 py-3 font-medium text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {productos.map(p => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{p.nombre}</td>
                  <td className="px-4 py-3 text-gray-600">${parseFloat(p.precio).toFixed(2)}</td>
                  <td className="px-4 py-3"><StockBadge stock={p.stock} /></td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button onClick={() => openEdit(p)}
                      className="text-xs px-3 py-1 rounded-lg border border-gray-200 hover:bg-gray-100 text-gray-600">
                      Editar
                    </button>
                    <button onClick={() => setToDelete(p)}
                      className="text-xs px-3 py-1 rounded-lg border border-red-200 hover:bg-red-50 text-red-500">
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modal && (
        <Modal title={modal.mode === 'create' ? 'Nuevo producto' : 'Editar producto'} onClose={closeModal}>
          <ProductoForm
            initial={modal.data}
            onSave={handleSave}
            onCancel={closeModal}
            loading={saving}
            error={saveError}
          />
        </Modal>
      )}

      {toDelete && (
        <ConfirmDialog
          message={`¿Eliminar el producto "${toDelete.nombre}"? Esta acción no se puede deshacer.`}
          onConfirm={handleDelete}
          onCancel={() => setToDelete(null)}
        />
      )}
    </div>
  )
}
