from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.pedido import Pedido, ItemPedido
from src.models.producto import Producto

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    try:
        # Obtener parámetros de consulta
        mesa = request.args.get('mesa', type=int)
        estado = request.args.get('estado')
        fecha = request.args.get('fecha')
        
        query = Pedido.query
        
        if mesa:
            query = query.filter_by(mesa=mesa)
        if estado:
            query = query.filter_by(estado=estado)
        if fecha:
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                query = query.filter(db.func.date(Pedido.fecha_hora) == fecha_obj)
            except ValueError:
                return jsonify({'success': False, 'message': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
        
        pedidos = query.order_by(Pedido.fecha_hora.desc()).all()
        
        return jsonify({
            'success': True,
            'pedidos': [pedido.to_dict() for pedido in pedidos]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@pedidos_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('mesa', 'productos', 'total')):
            return jsonify({'success': False, 'message': 'Mesa, productos y total son requeridos'}), 400
        
        if not data['productos']:
            return jsonify({'success': False, 'message': 'El pedido debe tener al menos un producto'}), 400
        
        # Crear el pedido
        pedido = Pedido(
            mesa=int(data['mesa']),
            total=float(data['total']),
            observaciones=data.get('observaciones', ''),
            estado='pendiente'
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obtener el ID del pedido
        
        # Agregar items del pedido
        for item_data in data['productos']:
            if not all(k in item_data for k in ('id', 'nombre', 'precio', 'cantidad')):
                return jsonify({'success': False, 'message': 'Cada producto debe tener id, nombre, precio y cantidad'}), 400
            
            # Verificar que el producto existe
            producto = Producto.query.get(item_data['id'])
            if not producto:
                return jsonify({'success': False, 'message': f'Producto con ID {item_data["id"]} no encontrado'}), 400
            
            if not producto.disponible:
                return jsonify({'success': False, 'message': f'Producto {producto.nombre} no está disponible'}), 400
            
            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                producto_id=item_data['id'],
                nombre_producto=item_data['nombre'],
                precio_unitario=float(item_data['precio']),
                cantidad=int(item_data['cantidad'])
            )
            
            db.session.add(item_pedido)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido creado exitosamente',
            'pedido': pedido.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:pedido_id>/estado', methods=['PUT'])
def update_estado_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        data = request.get_json()
        
        if not data or 'estado' not in data:
            return jsonify({'success': False, 'message': 'Estado es requerido'}), 400
        
        estados_validos = ['pendiente', 'preparando', 'listo', 'entregado']
        if data['estado'] not in estados_validos:
            return jsonify({'success': False, 'message': f'Estado debe ser uno de: {", ".join(estados_validos)}'}), 400
        
        pedido.estado = data['estado']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Estado del pedido actualizado exitosamente',
            'pedido': pedido.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido eliminado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@pedidos_bp.route('/pedidos/estadisticas', methods=['GET'])
def get_estadisticas():
    try:
        # Estadísticas básicas
        total_pedidos = Pedido.query.count()
        pedidos_pendientes = Pedido.query.filter_by(estado='pendiente').count()
        pedidos_preparando = Pedido.query.filter_by(estado='preparando').count()
        pedidos_listos = Pedido.query.filter_by(estado='listo').count()
        
        # Ventas del día
        hoy = datetime.now().date()
        ventas_hoy = db.session.query(db.func.sum(Pedido.total)).filter(
            db.func.date(Pedido.fecha_hora) == hoy
        ).scalar() or 0
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'total_pedidos': total_pedidos,
                'pedidos_pendientes': pedidos_pendientes,
                'pedidos_preparando': pedidos_preparando,
                'pedidos_listos': pedidos_listos,
                'ventas_hoy': float(ventas_hoy)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

