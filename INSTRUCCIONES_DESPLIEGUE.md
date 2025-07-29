# 🚀 Instrucciones de Despliegue - Diversum Cafetería v0.2

## ⚡ Despliegue Rápido (5 minutos)

### 1. Preparar el Entorno
```bash
# Descomprimir archivos
unzip diversum-cafeteria-v0.2.zip
cd diversum-cafeteria-v0.2

# Verificar que tienes Python 3.8+ y Node.js 16+
python --version
node --version
```

### 2. Configurar Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Probar backend
python src/main.py
```
✅ Backend funcionando en `http://localhost:5000`

### 3. Configurar Frontend
```bash
# En otra terminal
cd frontend

# Instalar dependencias
npm install

# Probar frontend
npm run dev
```
✅ Frontend funcionando en `http://localhost:5173`

### 4. Build para Producción
```bash
# En el directorio frontend
npm run build

# Copiar build al backend
cp -r dist/* ../backend/src/static/

# Ahora solo necesitas el backend
cd ../backend
python src/main.py
```
✅ Sistema completo en `http://localhost:5000`

---

## 🌐 Despliegue en Hosting

### Opción A: VPS/Servidor Dedicado (Recomendado)

#### 1. Subir Archivos
```bash
# Via SCP
scp -r diversum-cafeteria-v0.2 usuario@servidor:/var/www/

# Via Git (si tienes repositorio)
git clone tu-repositorio.git /var/www/diversum-cafeteria
```

#### 2. Instalar Dependencias del Sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# CentOS/RHEL
sudo yum install python3 python3-pip nginx
```

#### 3. Configurar la Aplicación
```bash
cd /var/www/diversum-cafeteria/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn  # Para producción

# Probar que funciona
python src/main.py
```

#### 4. Configurar Gunicorn
```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/diversum.service
```

Contenido del archivo:
```ini
[Unit]
Description=Diversum Cafeteria
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/diversum-cafeteria/backend
Environment="PATH=/var/www/diversum-cafeteria/backend/venv/bin"
ExecStart=/var/www/diversum-cafeteria/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable diversum
sudo systemctl start diversum
sudo systemctl status diversum
```

#### 5. Configurar Nginx
```bash
sudo nano /etc/nginx/sites-available/diversum
```

Contenido del archivo:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Archivos estáticos (opcional, para mejor rendimiento)
    location /static/ {
        alias /var/www/diversum-cafeteria/backend/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/diversum /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL con Let's Encrypt (Opcional)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

### Opción B: Heroku

#### 1. Preparar Archivos
```bash
# En el directorio raíz del proyecto
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT src.main:app" > Procfile
echo "python-3.11.0" > runtime.txt

# Mover requirements.txt al directorio raíz
cp backend/requirements.txt .

# Agregar gunicorn
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 2. Configurar Git
```bash
git init
git add .
git commit -m "Initial commit"
```

#### 3. Deploy en Heroku
```bash
# Instalar Heroku CLI
# Luego:
heroku create tu-app-diversum
git push heroku main
heroku open
```

---

### Opción C: Railway

#### 1. Conectar Repositorio
- Ir a [railway.app](https://railway.app)
- Conectar con GitHub
- Seleccionar repositorio

#### 2. Configurar Variables
```
PORT=5000
PYTHONPATH=/app/backend
```

#### 3. Deploy Automático
Railway detectará automáticamente Python y desplegará.

---

### Opción D: Render

#### 1. Crear `render.yaml`
```yaml
services:
  - type: web
    name: diversum-cafeteria
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app"
```

#### 2. Deploy
- Conectar repositorio en [render.com](https://render.com)
- Deploy automático

---

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Crear archivo .env en backend/
echo "SECRET_KEY=tu-clave-super-secreta-aqui" > backend/.env
echo "FLASK_ENV=production" >> backend/.env
echo "DATABASE_URL=sqlite:///app.db" >> backend/.env
```

### Base de Datos Externa (PostgreSQL)
```bash
# Instalar psycopg2
pip install psycopg2-binary

# Cambiar en main.py:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host:port/db'
```

### Dominio Personalizado
1. Comprar dominio
2. Configurar DNS apuntando a tu servidor
3. Configurar SSL
4. Actualizar configuración de Nginx

---

## 📊 Monitoreo y Mantenimiento

### Logs
```bash
# Ver logs del servicio
sudo journalctl -u diversum -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Automático
```bash
# Crear script de backup
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/diversum-cafeteria/backend/src/database/app.db /backups/diversum_$DATE.db
find /backups -name "diversum_*.db" -mtime +7 -delete
```

```bash
# Programar en crontab
crontab -e
# Agregar: 0 2 * * * /path/to/backup.sh
```

### Actualizaciones
```bash
# Actualizar código
cd /var/www/diversum-cafeteria
git pull origin main

# Reiniciar servicio
sudo systemctl restart diversum
```

---

## 🚨 Solución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status diversum

# Verificar logs
sudo journalctl -u diversum -n 50
```

### Error de Base de Datos
```bash
# Verificar permisos
sudo chown -R www-data:www-data /var/www/diversum-cafeteria

# Recrear base de datos
cd /var/www/diversum-cafeteria/backend
source venv/bin/activate
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"
```

### Error de Dependencias
```bash
# Reinstalar dependencias
cd /var/www/diversum-cafeteria/backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## ✅ Checklist Final

- [ ] Backend funcionando en puerto 5000
- [ ] Frontend compilado y copiado a static/
- [ ] Base de datos inicializada con productos
- [ ] Nginx configurado como proxy
- [ ] SSL configurado (si aplica)
- [ ] Servicio systemd funcionando
- [ ] Backup configurado
- [ ] Dominio apuntando al servidor

---

## 📞 URLs de Acceso Final

Una vez desplegado, tendrás acceso a:

- **🏠 Página principal**: `https://tu-dominio.com/`
- **🍽️ Panel de cocina**: `https://tu-dominio.com/api/admin/`
- **📊 Dashboard**: `https://tu-dominio.com/api/admin/dashboard`
- **🔌 API**: `https://tu-dominio.com/api/productos`

¡Tu sistema de cafetería digital está listo para recibir pedidos! 🎉

