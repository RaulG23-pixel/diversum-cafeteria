import { Routes, Route } from 'react-router-dom'
import SelectorMesa from './components/SelectorMesa'
import CartaDigital from './components/CartaDigital'
import { Toaster } from './components/ui/toaster'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      <Routes>
        <Route path="/" element={<SelectorMesa />} />
        <Route path="/mesa/:numeroMesa" element={<CartaDigital />} />
      </Routes>
      <Toaster />
    </div>
  )
}

export default App

