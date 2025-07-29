import { useNavigate } from 'react-router-dom'
import { Coffee, Users, ShoppingCart } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

function SelectorMesa() {
  const navigate = useNavigate()

  const mesas = Array.from({ length: 14 }, (_, i) => i + 1)

  const coloresMesas = [
    'bg-green-100 border-green-300 hover:bg-green-200',
    'bg-blue-100 border-blue-300 hover:bg-blue-200',
    'bg-yellow-100 border-yellow-300 hover:bg-yellow-200',
    'bg-purple-100 border-purple-300 hover:bg-purple-200',
    'bg-teal-100 border-teal-300 hover:bg-teal-200',
    'bg-pink-100 border-pink-300 hover:bg-pink-200',
    'bg-indigo-100 border-indigo-300 hover:bg-indigo-200',
    'bg-red-100 border-red-300 hover:bg-red-200',
    'bg-emerald-100 border-emerald-300 hover:bg-emerald-200',
    'bg-orange-100 border-orange-300 hover:bg-orange-200',
    'bg-cyan-100 border-cyan-300 hover:bg-cyan-200',
    'bg-lime-100 border-lime-300 hover:bg-lime-200',
    'bg-violet-100 border-violet-300 hover:bg-violet-200',
    'bg-amber-100 border-amber-300 hover:bg-amber-200'
  ]

  const seleccionarMesa = (numeroMesa) => {
    navigate(`/mesa/${numeroMesa}`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Coffee className="h-8 w-8 text-orange-600" />
            <h1 className="text-4xl font-bold text-gray-800">Diversum Cafetería</h1>
          </div>
          <p className="text-lg text-gray-600 mb-2">"Tu café con sabor a inclusión y cambio social"</p>
          <p className="text-gray-500">Selecciona tu mesa para comenzar</p>
        </div>

        {/* Selector de Mesas */}
        <Card className="mb-8">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2">
              <Users className="h-5 w-5" />
              Selecciona tu Mesa
            </CardTitle>
            <CardDescription>
              Haz clic en el número de tu mesa para acceder a la carta digital
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4">
              {mesas.map((mesa) => (
                <Button
                  key={mesa}
                  onClick={() => seleccionarMesa(mesa)}
                  className={`h-16 text-xl font-bold border-2 transition-all duration-200 ${
                    coloresMesas[mesa - 1]
                  } text-gray-800 hover:scale-105 hover:shadow-md`}
                  variant="outline"
                >
                  {mesa}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Características */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="text-center">
              <Coffee className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <CardTitle>Carta Digital</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-center">
                Explora nuestra amplia variedad de productos organizados por categorías
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Users className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <CardTitle>14 Mesas</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-center">
                Servicio personalizado para cada mesa con pedidos independientes
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <ShoppingCart className="h-8 w-8 text-orange-600 mx-auto mb-2" />
              <CardTitle>Pedido Fácil</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-center">
                Agrega productos al carrito y envía tu pedido directamente a cocina
              </CardDescription>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500">
          Sistema de Cafetería Digital v0.2 - Diversum
        </div>
      </div>
    </div>
  )
}

export default SelectorMesa

