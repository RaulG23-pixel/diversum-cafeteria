from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.producto import Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    try:
        productos = Producto.query.filter_by(disponible=True).all()
        return jsonify({
            'success': True,
            'productos': [producto.to_dict() for producto in productos]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        return jsonify({
            'success': True,
            'producto': producto.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = db.session.query(Producto.categoria).distinct().all()
        categorias_list = [cat[0] for cat in categorias]
        
        # Ordenar categorías en el orden deseado
        orden_categorias = [
            'Nuestras Tostas',
            'Bagels', 
            'Croissants/French Toast/Tortitas',
            'Frutas Naturales',
            'Menús Desayunos',
            'Caprichos Diversum',
            'Cafés/Tés/Chocolates/Bebidas'
        ]
        
        categorias_ordenadas = []
        for cat in orden_categorias:
            if cat in categorias_list:
                categorias_ordenadas.append(cat)
        
        # Agregar cualquier categoría que no esté en el orden predefinido
        for cat in categorias_list:
            if cat not in categorias_ordenadas:
                categorias_ordenadas.append(cat)
        
        return jsonify({
            'success': True,
            'categorias': categorias_ordenadas
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/productos/categoria/<categoria>', methods=['GET'])
def get_productos_por_categoria(categoria):
    try:
        productos = Producto.query.filter_by(categoria=categoria, disponible=True).all()
        return jsonify({
            'success': True,
            'productos': [producto.to_dict() for producto in productos]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/productos', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('nombre', 'precio', 'categoria')):
            return jsonify({'success': False, 'message': 'Nombre, precio y categoría son requeridos'}), 400
        
        producto = Producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=float(data['precio']),
            categoria=data['categoria'],
            disponible=data.get('disponible', True)
        )
        
        db.session.add(producto)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Producto creado exitosamente',
            'producto': producto.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        data = request.get_json()
        
        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        if 'precio' in data:
            producto.precio = float(data['precio'])
        if 'categoria' in data:
            producto.categoria = data['categoria']
        if 'disponible' in data:
            producto.disponible = data['disponible']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Producto actualizado exitosamente',
            'producto': producto.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@productos_bp.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        db.session.delete(producto)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Producto eliminado exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

