from flask import Blueprint, request, jsonify, render_template_string
from datetime import datetime, timedelta
from src.models.user import db
from src.models.pedido import Pedido, ItemPedido
from src.models.producto import Producto

admin_bp = Blueprint('admin', __name__)

# Panel de administración simple en HTML
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Cocina - Diversum</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .header { background-color: #ff6b35; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; color: #ff6b35; }
        .pedidos { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .pedido { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .pedido-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .mesa { font-size: 1.2em; font-weight: bold; }
        .estado { padding: 5px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
        .pendiente { background-color: #ffeaa7; color: #d63031; }
        .preparando { background-color: #74b9ff; color: white; }
        .listo { background-color: #00b894; color: white; }
        .entregado { background-color: #ddd; color: #666; }
        .items { margin: 10px 0; }
        .item { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eee; }
        .total { font-weight: bold; font-size: 1.1em; color: #ff6b35; margin-top: 10px; }
        .observaciones { background-color: #f8f9fa; padding: 8px; border-radius: 4px; margin-top: 10px; font-style: italic; }
        .acciones { margin-top: 15px; display: flex; gap: 10px; }
        .btn { padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em; }
        .btn-preparar { background-color: #74b9ff; color: white; }
        .btn-listo { background-color: #00b894; color: white; }
        .btn-entregar { background-color: #636e72; color: white; }
        .refresh-btn { background-color: #ff6b35; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🍽️ Panel de Cocina - Diversum Cafetería</h1>
        <p>Gestión de pedidos en tiempo real</p>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number" id="pendientes">{{ stats.pendientes }}</div>
            <div>Pendientes</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="preparando">{{ stats.preparando }}</div>
            <div>Preparando</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="listos">{{ stats.listos }}</div>
            <div>Listos</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">€{{ "%.2f"|format(stats.ventas_hoy) }}</div>
            <div>Ventas Hoy</div>
        </div>
    </div>
    
    <div class="pedidos">
        {% for pedido in pedidos %}
        <div class="pedido">
            <div class="pedido-header">
                <span class="mesa">Mesa {{ pedido.mesa }}</span>
                <span class="estado {{ pedido.estado }}">{{ pedido.estado.upper() }}</span>
            </div>
            <div style="font-size: 0.9em; color: #666; margin-bottom: 10px;">
                {{ pedido.fecha_hora.strftime('%H:%M') }} - Pedido #{{ pedido.id }}
            </div>
            <div class="items">
                {% for item in pedido.items %}
                <div class="item">
                    <span>{{ item.cantidad }}x {{ item.nombre_producto }}</span>
                    <span>€{{ "%.2f"|format(item.precio_unitario * item.cantidad) }}</span>
                </div>
                {% endfor %}
            </div>
            {% if pedido.observaciones %}
            <div class="observaciones">
                📝 {{ pedido.observaciones }}
            </div>
            {% endif %}
            <div class="total">
                Total: €{{ "%.2f"|format(pedido.total) }}
            </div>
            <div class="acciones">
                {% if pedido.estado == 'pendiente' %}
                <button class="btn btn-preparar" onclick="cambiarEstado({{ pedido.id }}, 'preparando')">
                    👨‍🍳 Preparar
                </button>
                {% elif pedido.estado == 'preparando' %}
                <button class="btn btn-listo" onclick="cambiarEstado({{ pedido.id }}, 'listo')">
                    ✅ Listo
                </button>
                {% elif pedido.estado == 'listo' %}
                <button class="btn btn-entregar" onclick="cambiarEstado({{ pedido.id }}, 'entregado')">
                    🚚 Entregado
                </button>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <script>
        function cambiarEstado(pedidoId, nuevoEstado) {
            fetch(`/api/pedidos/${pedidoId}/estado`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ estado: nuevoEstado })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al actualizar el estado');
            });
        }
        
        // Auto-refresh cada 30 segundos
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

@admin_bp.route('/', methods=['GET'])
@admin_bp.route('/cocina', methods=['GET'])
def panel_cocina():
    try:
        # Obtener pedidos activos (no entregados)
        pedidos = Pedido.query.filter(Pedido.estado.in_(['pendiente', 'preparando', 'listo'])).order_by(Pedido.fecha_hora.asc()).all()
        
        # Estadísticas
        stats = {
            'pendientes': Pedido.query.filter_by(estado='pendiente').count(),
            'preparando': Pedido.query.filter_by(estado='preparando').count(),
            'listos': Pedido.query.filter_by(estado='listo').count(),
            'ventas_hoy': 0
        }
        
        # Ventas del día
        hoy = datetime.now().date()
        ventas_hoy = db.session.query(db.func.sum(Pedido.total)).filter(
            db.func.date(Pedido.fecha_hora) == hoy
        ).scalar()
        stats['ventas_hoy'] = float(ventas_hoy) if ventas_hoy else 0
        
        return render_template_string(ADMIN_TEMPLATE, pedidos=pedidos, stats=stats)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        # Estadísticas generales
        total_pedidos = Pedido.query.count()
        total_productos = Producto.query.count()
        
        # Pedidos por estado
        pedidos_por_estado = {}
        estados = ['pendiente', 'preparando', 'listo', 'entregado']
        for estado in estados:
            pedidos_por_estado[estado] = Pedido.query.filter_by(estado=estado).count()
        
        # Ventas por día (últimos 7 días)
        ventas_por_dia = []
        for i in range(7):
            fecha = datetime.now().date() - timedelta(days=i)
            ventas = db.session.query(db.func.sum(Pedido.total)).filter(
                db.func.date(Pedido.fecha_hora) == fecha
            ).scalar() or 0
            ventas_por_dia.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'ventas': float(ventas)
            })
        
        # Productos más vendidos
        productos_vendidos = db.session.query(
            ItemPedido.nombre_producto,
            db.func.sum(ItemPedido.cantidad).label('total_vendido')
        ).group_by(ItemPedido.nombre_producto).order_by(
            db.func.sum(ItemPedido.cantidad).desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'dashboard': {
                'total_pedidos': total_pedidos,
                'total_productos': total_productos,
                'pedidos_por_estado': pedidos_por_estado,
                'ventas_por_dia': ventas_por_dia,
                'productos_mas_vendidos': [
                    {'nombre': p[0], 'cantidad': p[1]} for p in productos_vendidos
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/reset-database', methods=['POST'])
def reset_database():
    try:
        # CUIDADO: Esto elimina todos los datos
        db.drop_all()
        db.create_all()
        
        return jsonify({
            'success': True,
            'message': 'Base de datos reiniciada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

