import { useEffect, useState } from 'react'
import { getClientes, createCliente, updateCliente, deleteCliente } from '../api/clientes'
import Modal from '../components/ui/Modal'
import ConfirmDialog from '../components/ui/ConfirmDialog'

const EMPTY = { nombre: '', correo: '', telefono: '', direccion: '' }

function ClienteForm({ initial, onSave, onCancel, loading, error }) {
  const [form, setForm] = useState(initial)
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(form)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      {error && <p className="text-red-500 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>}
      <div>
        <label className="text-xs font-medium text-gray-500 block mb-1">Nombre *</label>
        <input value={form.nombre} onChange={set('nombre')} required
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div>
        <label className="text-xs font-medium text-gray-500 block mb-1">Correo *</label>
        <input type="email" value={form.correo} onChange={set('correo')} required
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div>
        <label className="text-xs font-medium text-gray-500 block mb-1">Teléfono</label>
        <input value={form.telefono} onChange={set('telefono')}
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div>
        <label className="text-xs font-medium text-gray-500 block mb-1">Dirección</label>
        <input value={form.direccion} onChange={set('direccion')}
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
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

export default function Clientes() {
  const [clientes, setClientes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [modal, setModal] = useState(null)   // null | { mode: 'create'|'edit', data }
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState(null)
  const [toDelete, setToDelete] = useState(null)

  const load = () => {
    setLoading(true)
    getClientes()
      .then(setClientes)
      .catch(() => setError('No se pudieron cargar los clientes'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    setLoading(true)
    getClientes()
      .then(setClientes)
      .catch(() => setError('No se pudieron cargar los clientes'))
      .finally(() => setLoading(false))
  }, [])

  const openCreate = () => { setSaveError(null); setModal({ mode: 'create', data: EMPTY }) }
  const openEdit   = (c) => { setSaveError(null); setModal({ mode: 'edit',   data: { nombre: c.nombre, correo: c.correo, telefono: c.telefono || '', direccion: c.direccion || '' }, id: c.id }) }
  const closeModal = () => setModal(null)

  const handleSave = async (form) => {
    setSaving(true); setSaveError(null)
    try {
      if (modal.mode === 'create') await createCliente(form)
      else await updateCliente(modal.id, form)
      closeModal(); load()
    } catch (e) {
      setSaveError(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    try {
      await deleteCliente(toDelete.id)
      setToDelete(null); load()
    } catch (e) {
      alert(e.message)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-700">Clientes</h1>
        <button onClick={openCreate}
          className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-1">
          + Nuevo cliente
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        {loading && <p className="text-sm text-gray-400 p-5">Cargando...</p>}
        {error   && <p className="text-sm text-red-500 p-5">{error}</p>}
        {!loading && !error && clientes.length === 0 && (
          <p className="text-sm text-gray-400 p-5">No hay clientes registrados.</p>
        )}
        {!loading && clientes.length > 0 && (
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr className="text-left text-gray-500 text-xs uppercase tracking-wide">
                <th className="px-4 py-3 font-medium">Nombre</th>
                <th className="px-4 py-3 font-medium">Correo</th>
                <th className="px-4 py-3 font-medium">Teléfono</th>
                <th className="px-4 py-3 font-medium">Dirección</th>
                <th className="px-4 py-3 font-medium text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {clientes.map(c => (
                <tr key={c.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{c.nombre}</td>
                  <td className="px-4 py-3 text-gray-500">{c.correo}</td>
                  <td className="px-4 py-3 text-gray-500">{c.telefono || '—'}</td>
                  <td className="px-4 py-3 text-gray-500">{c.direccion || '—'}</td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button onClick={() => openEdit(c)}
                      className="text-xs px-3 py-1 rounded-lg border border-gray-200 hover:bg-gray-100 text-gray-600">
                      Editar
                    </button>
                    <button onClick={() => setToDelete(c)}
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
        <Modal title={modal.mode === 'create' ? 'Nuevo cliente' : 'Editar cliente'} onClose={closeModal}>
          <ClienteForm
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
          message={`¿Eliminar al cliente "${toDelete.nombre}"? Esta acción no se puede deshacer.`}
          onConfirm={handleDelete}
          onCancel={() => setToDelete(null)}
        />
      )}
    </div>
  )
}
