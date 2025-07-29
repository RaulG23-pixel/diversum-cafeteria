from datetime import datetime
from src.models.user import db

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.Integer, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, preparando, listo, entregado
    
    # Relación con items del pedido
    items = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'mesa': self.mesa,
            'fecha_hora': self.fecha_hora.isoformat(),
            'total': self.total,
            'observaciones': self.observaciones,
            'estado': self.estado,
            'items': [item.to_dict() for item in self.items]
        }
    
    def __repr__(self):
        return f'<Pedido {self.id} - Mesa {self.mesa}>'

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    nombre_producto = db.Column(db.String(200), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    
    # Relación con producto
    producto = db.relationship('Producto', backref='items_pedido')
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'nombre_producto': self.nombre_producto,
            'precio_unitario': self.precio_unitario,
            'cantidad': self.cantidad,
            'subtotal': self.precio_unitario * self.cantidad
        }
    
    def __repr__(self):
        return f'<ItemPedido {self.nombre_producto} x{self.cantidad}>'

