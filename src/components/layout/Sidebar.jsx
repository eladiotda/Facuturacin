import { NavLink } from 'react-router-dom'

const links = [
  { to: '/',          icon: '🏠', label: 'Inicio' },
  { to: '/clientes',  icon: '👥', label: 'Clientes' },
  { to: '/productos', icon: '📦', label: 'Productos' },
  { to: '/facturas',  icon: '🧾', label: 'Facturas' },
]

export default function Sidebar() {
  return (
    <aside className="w-16 min-h-screen bg-gray-900 flex flex-col items-center py-4 gap-2 shrink-0">
      {links.map(({ to, icon, label }) => (
        <NavLink
          key={to}
          to={to}
          end={to === '/'}
          title={label}
          className={({ isActive }) =>
            `w-12 h-12 flex items-center justify-center rounded-xl text-xl transition-colors
             ${isActive ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-700 hover:text-white'}`
          }
        >
          {icon}
        </NavLink>
      ))}
    </aside>
  )
}
