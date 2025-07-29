# 🍽️ Sistema de Cafetería Digital Diversum v0.2

Sistema completo de carta digital para cafeterías con gestión de pedidos en tiempo real.

## 📋 Características

- **14 mesas independientes** con gestión de pedidos separada
- **7 categorías de productos** organizadas según la carta real
- **101 productos únicos** con precios y descripciones
- **Sistema de carrito** con gestión de cantidades
- **Panel de cocina** en tiempo real para gestión de pedidos
- **Interfaz responsive** optimizada para móviles y tablets
- **API REST completa** para integración con otros sistemas

## 🏗️ Arquitectura

### Frontend (React + Vite)
- **React 18** con hooks modernos
- **Tailwind CSS** para estilos
- **Framer Motion** para animaciones
- **React Router** para navegación
- **Lucide React** para iconos

### Backend (Flask + SQLAlchemy)
- **Flask 3.0** como framework web
- **SQLAlchemy** para ORM y base de datos
- **SQLite** como base de datos (fácil de cambiar)
- **Flask-CORS** para permitir requests del frontend

## 🚀 Instalación y Despliegue

### Requisitos Previos
- Python 3.8+
- Node.js 16+
- npm o yarn

### 1. Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\\Scripts\\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python src/main.py
```

El backend estará disponible en `http://localhost:5000`

### 2. Configurar el Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### 3. Build para Producción

```bash
# En el directorio frontend
npm run build

# Copiar archivos build al backend
cp -r dist/* ../backend/src/static/
```

Después del build, el backend servirá tanto la API como el frontend desde `http://localhost:5000`

## 🌐 Despliegue en Hosting

### Opción 1: Servidor VPS (Recomendado)

1. **Subir archivos al servidor**
2. **Instalar dependencias del backend**
3. **Configurar servidor web (Nginx + Gunicorn)**

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

4. **Configurar Nginx como proxy reverso**

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Opción 2: Plataformas Cloud

#### Heroku
1. Crear `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
```

2. Configurar variables de entorno
3. Deploy con Git

#### Railway/Render
1. Conectar repositorio
2. Configurar build commands
3. Deploy automático

### Opción 3: Hosting Compartido con Python

1. Subir archivos via FTP/SFTP
2. Instalar dependencias en el hosting
3. Configurar WSGI según el proveedor

## 📱 URLs de Acceso

### Para Clientes
- **Página principal**: `https://tu-dominio.com/`
- **Mesa específica**: `https://tu-dominio.com/mesa/[1-14]`

### Para Personal de Cocina
- **Panel de cocina**: `https://tu-dominio.com/api/admin/`
- **Dashboard**: `https://tu-dominio.com/api/admin/dashboard`

### API Endpoints
- **Productos**: `GET /api/productos`
- **Categorías**: `GET /api/categorias`
- **Crear pedido**: `POST /api/pedidos`
- **Ver pedidos**: `GET /api/pedidos`
- **Cambiar estado**: `PUT /api/pedidos/{id}/estado`

## 🔧 Configuración

### Variables de Entorno (Opcional)
```bash
export FLASK_ENV=production
export SECRET_KEY=tu-clave-secreta-aqui
export DATABASE_URL=sqlite:///app.db
```

### Personalización
- **Productos**: Modificar la lista en `backend/src/main.py`
- **Colores**: Editar `frontend/src/index.css`
- **Logo**: Reemplazar favicon en `frontend/public/`

## 📊 Base de Datos

### Estructura
- **productos**: Catálogo de productos con precios
- **pedidos**: Pedidos realizados por mesa
- **items_pedido**: Productos específicos de cada pedido
- **users**: Usuarios del sistema (opcional)

### Backup
```bash
# Crear backup
cp backend/src/database/app.db backup_$(date +%Y%m%d).db

# Restaurar backup
cp backup_20240101.db backend/src/database/app.db
```

## 🛠️ Desarrollo

### Estructura del Proyecto
```
diversum-cafeteria-v0.2/
├── frontend/                 # Aplicación React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/          # Hooks personalizados
│   │   └── lib/            # Utilidades
│   └── public/             # Archivos estáticos
├── backend/                 # API Flask
│   ├── src/
│   │   ├── models/         # Modelos de base de datos
│   │   ├── routes/         # Rutas de la API
│   │   └── static/         # Frontend compilado
│   └── requirements.txt    # Dependencias Python
└── README.md               # Este archivo
```

### Comandos Útiles

```bash
# Reiniciar base de datos
curl -X POST http://localhost:5000/api/admin/reset-database

# Ver estadísticas
curl http://localhost:5000/api/admin/dashboard

# Crear producto
curl -X POST http://localhost:5000/api/productos \\
  -H "Content-Type: application/json" \\
  -d '{"nombre":"Nuevo Producto","precio":5.50,"categoria":"Nuestras Tostas"}'
```

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
# Reinstalar dependencias
cd frontend && npm install
cd backend && pip install -r requirements.txt
```

### Error: "Database locked"
```bash
# Reiniciar servidor backend
pkill -f python
python backend/src/main.py
```

### Error: "CORS policy"
- Verificar que Flask-CORS esté instalado
- Comprobar configuración en `main.py`

## 📞 Soporte

Para problemas técnicos:
1. Verificar logs del servidor
2. Comprobar conexión a base de datos
3. Revisar configuración de CORS
4. Validar estructura de archivos

## 📄 Licencia

Este proyecto está desarrollado para Diversum Cafetería.

---

**¡Tu sistema de cafetería digital está listo para funcionar!** ☕️

