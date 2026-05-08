import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getClientes } from '../api/clientes'
import { getProductos } from '../api/productos'
import { getFacturas } from '../api/facturas'

function StatCard({ icon, label, value, to, color }) {
  return (
    <Link to={to} className={`rounded-xl p-5 flex items-center gap-4 shadow-sm border border-gray-100 bg-white hover:shadow-md transition-shadow`}>
      <span className={`text-3xl p-3 rounded-xl ${color}`}>{icon}</span>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-800">{value ?? '—'}</p>
      </div>
    </Link>
  )
}

export default function Dashboard() {
  const [clientes, setClientes] = useState([])
  const [productos, setProductos] = useState([])
  const [facturas, setFacturas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getClientes(), getProductos(), getFacturas()])
      .then(([c, p, f]) => { setClientes(c); setProductos(p); setFacturas(f) })
      .catch(() => setError('No se pudo conectar con el servidor'))
      .finally(() => setLoading(false))
  }, [])

  const totalFacturado = facturas.reduce((sum, f) => sum + parseFloat(f.total || 0), 0)
  const stockBajo = productos.filter(p => p.stock <= 2)
  const recientes = [...facturas].sort((a, b) => new Date(b.fecha_emision) - new Date(a.fecha_emision)).slice(0, 5)

  if (loading) return <p className="text-gray-400 text-sm">Cargando...</p>
  if (error)   return <p className="text-red-500 text-sm">{error}</p>

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold text-gray-700">Dashboard</h1>

      {/* Cards de resumen */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard icon="👥" label="Clientes"  value={clientes.length}  to="/clientes"  color="bg-blue-50" />
        <StatCard icon="📦" label="Productos" value={productos.length} to="/productos" color="bg-green-50" />
        <StatCard icon="🧾" label="Facturas"  value={facturas.length}  to="/facturas"  color="bg-purple-50" />
        <StatCard
          icon="💰"
          label="Total facturado"
          value={`$${totalFacturado.toFixed(2)}`}
          to="/facturas"
          color="bg-yellow-50"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Facturas recientes */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <h2 className="text-sm font-semibold text-gray-600 mb-4">Facturas recientes</h2>
          {recientes.length === 0 ? (
            <p className="text-sm text-gray-400">Sin facturas aún.</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-400 border-b border-gray-100">
                  <th className="pb-2 font-medium">Número</th>
                  <th className="pb-2 font-medium">Cliente</th>
                  <th className="pb-2 font-medium">Fecha</th>
                  <th className="pb-2 font-medium text-right">Total</th>
                </tr>
              </thead>
              <tbody>
                {recientes.map(f => (
                  <tr key={f.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-2 text-blue-600 font-medium">{f.numero}</td>
                    <td className="py-2 text-gray-600">{f.cliente?.nombre ?? '—'}</td>
                    <td className="py-2 text-gray-400">
                      {new Date(f.fecha_emision).toLocaleDateString('es-CO')}
                    </td>
                    <td className="py-2 text-right font-semibold text-gray-700">${parseFloat(f.total).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Stock bajo */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <h2 className="text-sm font-semibold text-gray-600 mb-4">⚠️ Stock bajo</h2>
          {stockBajo.length === 0 ? (
            <p className="text-sm text-gray-400">Todo en orden.</p>
          ) : (
            <ul className="space-y-2">
              {stockBajo.map(p => (
                <li key={p.id} className="flex items-center justify-between text-sm">
                  <span className="text-gray-700">{p.nombre}</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${p.stock === 0 ? 'bg-red-100 text-red-600' : 'bg-yellow-100 text-yellow-700'}`}>
                    {p.stock === 0 ? 'Sin stock' : `x${p.stock}`}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
