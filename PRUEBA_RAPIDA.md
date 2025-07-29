# ⚡ Prueba Rápida - 2 Minutos

## 🚀 Verificar que Todo Funciona

### 1. Probar Backend (30 segundos)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python src/main.py
```

✅ Deberías ver: `Running on http://127.0.0.1:5000`

### 2. Probar Frontend (1 minuto)
```bash
# En otra terminal
cd frontend
npm install
npm run dev
```

✅ Deberías ver: `Local: http://localhost:5173/`

### 3. Verificar Funcionamiento (30 segundos)

1. **Abrir**: `http://localhost:5173`
2. **Ver**: Selector de 14 mesas con logo Diversum
3. **Hacer clic**: En cualquier mesa (ej: Mesa 5)
4. **Ver**: 7 categorías de productos
5. **Hacer clic**: En "Cafés/Tés/Chocolates/Bebidas"
6. **Ver**: Lista de cafés con precios
7. **Hacer clic**: "Agregar al carrito" en cualquier producto
8. **Ver**: Botón flotante del carrito con contador "1"
9. **Hacer clic**: En el botón del carrito
10. **Ver**: Modal con el producto y botón "Enviar a Cocina"

### 4. Verificar Panel de Cocina
1. **Abrir**: `http://localhost:5000/api/admin/`
2. **Ver**: Panel de cocina con estadísticas
3. **Enviar pedido** desde el frontend
4. **Refrescar** panel de cocina
5. **Ver**: Nuevo pedido aparece

---

## 🎯 Si Todo Funciona:
- ✅ Backend: OK
- ✅ Frontend: OK  
- ✅ Base de datos: OK
- ✅ API: OK
- ✅ Panel de cocina: OK

**¡Listo para desplegar!** 🚀

---

## 🚨 Si Algo Falla:

### Error: "Module not found"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
npm install
```

### Error: "Port already in use"
```bash
# Cambiar puerto en main.py línea final:
# app.run(host='0.0.0.0', port=5001, debug=True)
```

### Error: "Database error"
```bash
# Eliminar base de datos y recrear
rm backend/src/database/app.db
python backend/src/main.py
```

---

## 📱 URLs de Prueba

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5000  
- **API Productos**: http://localhost:5000/api/productos
- **Panel Cocina**: http://localhost:5000/api/admin/
- **Mesa 1**: http://localhost:5173/mesa/1

---

**¡En 2 minutos sabrás si todo funciona perfectamente!** ⏱️

