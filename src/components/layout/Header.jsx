export default function Header() {
  const fecha = new Date().toLocaleDateString('es-CO', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  })

  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center px-6 justify-between shrink-0">
      <span className="font-semibold text-gray-800 text-lg tracking-tight">
        TDEA Facturación
      </span>
      <span className="text-sm text-gray-400 capitalize">{fecha}</span>
    </header>
  )
}
