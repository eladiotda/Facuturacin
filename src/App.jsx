import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Clientes from './pages/Clientes'
import Productos from './pages/Productos'
import Facturas from './pages/Facturas'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index           element={<Dashboard />} />
          <Route path="clientes"  element={<Clientes />} />
          <Route path="productos" element={<Productos />} />
          <Route path="facturas"  element={<Facturas />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
