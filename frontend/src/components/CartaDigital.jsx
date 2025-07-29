import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Coffee, ShoppingCart, Plus, Minus, Check, Clock, ChefHat } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Textarea } from './ui/textarea'
import { useToast } from '../hooks/use-toast'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = '/api'

function CartaDigital() {
  const { numeroMesa } = useParams()
  const { toast } = useToast()
  
  const [productos, setProductos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [categoriaActiva, setCategoriaActiva] = useState('')
  const [carrito, setCarrito] = useState([])
  const [observaciones, setObservaciones] = useState('')
  const [cargando, setCargando] = useState(true)
  const [enviandoPedido, setEnviandoPedido] = useState(false)
  const [mostrarCarrito, setMostrarCarrito] = useState(false)

  useEffect(() => {
    cargarDatos()
  }, [])

  const cargarDatos = async () => {
    try {
      setCargando(true)
      
      // Cargar productos
      const productosResponse = await fetch(`${API_BASE}/productos`)
      const productosData = await productosResponse.json()
      
      if (productosData.success) {
        setProductos(productosData.productos)
      }
      
      // Cargar categorías
      const categoriasResponse = await fetch(`${API_BASE}/categorias`)
      const categoriasData = await categoriasResponse.json()
      
      if (categoriasData.success) {
        setCategorias(categoriasData.categorias)
        if (categoriasData.categorias.length > 0) {
          setCategoriaActiva(categoriasData.categorias[0])
        }
      }
    } catch (error) {
      console.error('Error cargando datos:', error)
      toast({
        title: "Error",
        description: "No se pudieron cargar los datos. Inténtalo de nuevo.",
        variant: "destructive"
      })
    } finally {
      setCargando(false)
    }
  }

  const productosFiltrados = productos.filter(p => p.categoria === categoriaActiva)

  const agregarAlCarrito = (producto) => {
    setCarrito(prev => {
      const existente = prev.find(item => item.id === producto.id)
      if (existente) {
        return prev.map(item =>
          item.id === producto.id
            ? { ...item, cantidad: item.cantidad + 1 }
            : item
        )
      }
      return [...prev, { ...producto, cantidad: 1 }]
    })

    toast({
      title: "Producto agregado",
      description: `${producto.nombre} se agregó al carrito`,
    })
  }

  const modificarCantidad = (id, nuevaCantidad) => {
    if (nuevaCantidad === 0) {
      setCarrito(prev => prev.filter(item => item.id !== id))
    } else {
      setCarrito(prev =>
        prev.map(item =>
          item.id === id ? { ...item, cantidad: nuevaCantidad } : item
        )
      )
    }
  }

  const calcularTotal = () => {
    return carrito.reduce((total, item) => total + (item.precio * item.cantidad), 0)
  }

  const enviarPedido = async () => {
    if (carrito.length === 0) {
      toast({
        title: "Carrito vacío",
        description: "Agrega productos antes de enviar el pedido",
        variant: "destructive"
      })
      return
    }

    try {
      setEnviandoPedido(true)
      
      const pedido = {
        mesa: parseInt(numeroMesa),
        productos: carrito.map(item => ({
          id: item.id,
          nombre: item.nombre,
          precio: item.precio,
          cantidad: item.cantidad
        })),
        observaciones: observaciones,
        total: calcularTotal()
      }

      const response = await fetch(`${API_BASE}/pedidos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(pedido)
      })

      const data = await response.json()

      if (data.success) {
        toast({
          title: "¡Pedido enviado!",
          description: `Tu pedido para la mesa ${numeroMesa} se envió a cocina`,
        })
        
        // Limpiar carrito
        setCarrito([])
        setObservaciones('')
        setMostrarCarrito(false)
      } else {
        throw new Error(data.message || 'Error al enviar pedido')
      }
    } catch (error) {
      console.error('Error enviando pedido:', error)
      toast({
        title: "Error",
        description: "No se pudo enviar el pedido. Inténtalo de nuevo.",
        variant: "destructive"
      })
    } finally {
      setEnviandoPedido(false)
    }
  }

  const coloresCategorias = {
    'Nuestras Tostas': 'bg-green-100 text-green-800 border-green-300',
    'Bagels': 'bg-blue-100 text-blue-800 border-blue-300',
    'Croissants/French Toast/Tortitas': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'Frutas Naturales': 'bg-purple-100 text-purple-800 border-purple-300',
    'Menús Desayunos': 'bg-teal-100 text-teal-800 border-teal-300',
    'Caprichos Diversum': 'bg-pink-100 text-pink-800 border-pink-300',
    'Cafés/Tés/Chocolates/Bebidas': 'bg-indigo-100 text-indigo-800 border-indigo-300'
  }

  if (cargando) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 flex items-center justify-center">
        <div className="text-center">
          <Coffee className="h-12 w-12 text-orange-600 mx-auto mb-4 animate-spin" />
          <p className="text-lg text-gray-600">Cargando carta digital...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Coffee className="h-8 w-8 text-orange-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Diversum</h1>
                <p className="text-sm text-gray-600">Mesa {numeroMesa}</p>
              </div>
            </div>
            <p className="text-gray-600 hidden sm:block">
              Selecciona tus productos favoritos y realiza tu pedido
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* Categorías */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2 justify-center">
            {categorias.map((categoria) => (
              <Button
                key={categoria}
                onClick={() => setCategoriaActiva(categoria)}
                variant={categoriaActiva === categoria ? "default" : "outline"}
                className={`${
                  categoriaActiva === categoria 
                    ? coloresCategorias[categoria] || 'bg-orange-100 text-orange-800'
                    : 'hover:bg-gray-100'
                } border transition-all duration-200`}
              >
                {categoria}
              </Button>
            ))}
          </div>
        </div>

        {/* Productos */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
          <AnimatePresence mode="wait">
            {productosFiltrados.map((producto) => (
              <motion.div
                key={producto.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow duration-200">
                  <CardHeader>
                    <CardTitle className="text-lg">{producto.nombre}</CardTitle>
                    <CardDescription className="text-sm">
                      {producto.descripcion}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary" className="text-lg font-bold">
                        €{producto.precio.toFixed(2)}
                      </Badge>
                      <Button
                        onClick={() => agregarAlCarrito(producto)}
                        className="bg-orange-600 hover:bg-orange-700 text-white"
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Agregar al carrito
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Carrito flotante */}
      {carrito.length > 0 && (
        <div className="fixed bottom-4 right-4 z-50">
          <Button
            onClick={() => setMostrarCarrito(true)}
            className="bg-orange-600 hover:bg-orange-700 text-white rounded-full h-16 w-16 shadow-lg"
          >
            <div className="relative">
              <ShoppingCart className="h-6 w-6" />
              <Badge className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full h-6 w-6 flex items-center justify-center text-xs">
                {carrito.reduce((total, item) => total + item.cantidad, 0)}
              </Badge>
            </div>
          </Button>
        </div>
      )}

      {/* Modal del carrito */}
      {mostrarCarrito && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md max-h-[80vh] overflow-y-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="h-5 w-5" />
                Tu Pedido - Mesa {numeroMesa}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {carrito.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-sm">{item.nombre}</h4>
                    <p className="text-sm text-gray-600">€{item.precio.toFixed(2)} c/u</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => modificarCantidad(item.id, item.cantidad - 1)}
                    >
                      <Minus className="h-3 w-3" />
                    </Button>
                    <span className="w-8 text-center">{item.cantidad}</span>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => modificarCantidad(item.id, item.cantidad + 1)}
                    >
                      <Plus className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              ))}

              <div className="space-y-3">
                <Textarea
                  placeholder="Observaciones especiales (opcional)"
                  value={observaciones}
                  onChange={(e) => setObservaciones(e.target.value)}
                  className="resize-none"
                />

                <div className="flex justify-between items-center text-lg font-bold">
                  <span>Total:</span>
                  <span>€{calcularTotal().toFixed(2)}</span>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setMostrarCarrito(false)}
                    className="flex-1"
                  >
                    Continuar
                  </Button>
                  <Button
                    onClick={enviarPedido}
                    disabled={enviandoPedido}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                  >
                    {enviandoPedido ? (
                      <>
                        <Clock className="h-4 w-4 mr-2 animate-spin" />
                        Enviando...
                      </>
                    ) : (
                      <>
                        <ChefHat className="h-4 w-4 mr-2" />
                        Enviar a Cocina
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

export default CartaDigital

