import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.productos import productos_bp
from src.routes.pedidos import pedidos_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'diversum-cafeteria-secret-key-2024'

# Habilitar CORS para todas las rutas
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(productos_bp, url_prefix='/api')
app.register_blueprint(pedidos_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Importar todos los modelos para que se creen las tablas
from src.models.producto import Producto
from src.models.pedido import Pedido, ItemPedido

with app.app_context():
    db.create_all()
    
    # Inicializar productos de Diversum si no existen
    if Producto.query.count() == 0:
        productos_diversum = [
            # NUESTRAS TOSTAS
            Producto(nombre="Tosta de Tomate, AOVE y Cebollino", descripcion="Pan artesano con tomate, aceite de oliva virgen extra y cebollino", precio=3.10, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Tomate y Paleta Ibérica", descripcion="Pan artesano con tomate y paleta ibérica", precio=5.75, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Tomate, Aguacate y Paleta Ibérica", descripcion="Pan artesano con tomate, aguacate y paleta ibérica", precio=6.60, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Aguacate, Tomate y Semillas de Amapola", descripcion="Pan artesano con aguacate, tomate y semillas de amapola", precio=4.30, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Queso Crema, Jamón Cocido y Tomate", descripcion="Pan artesano con queso crema, jamón cocido y tomate", precio=4.60, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Queso Crema, Aguacate y Sésamo", descripcion="Pan artesano con queso crema, aguacate y sésamo", precio=4.60, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta Cubana", descripcion="Milhojas de lacón braseado, queso de Arzúa, pepinillos, mostaza tradicional y paleta ibérica", precio=6.60, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta Vegana", descripcion="Base de hummus casero con AOVE, champiñones salteados al Pedro Ximénez, microbrotes y granada", precio=5.95, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta Calabizo (Vegana)", descripcion="Base de hummus casero con AOVE, aguacate, cherries, cebolla morada y calabizo", precio=5.95, categoria="Nuestras Tostas"),
            Producto(nombre="Tosta de Salmón, Queso Crema y Aguacate", descripcion="Pan artesano con salmón, queso crema y aguacate", precio=8.00, categoria="Nuestras Tostas"),
            Producto(nombre="Sandwich de Queso, Bacon y Huevos Revueltos", descripcion="Elige tu pan: Masa madre con Quinoa o Cereales", precio=6.10, categoria="Nuestras Tostas"),
            Producto(nombre="Sandwich de Cebolla Caramelizada, Champiñones y Queso", descripcion="Cebolla caramelizada, champiñones al Pedro Ximénez, cherries y queso", precio=6.10, categoria="Nuestras Tostas"),
            Producto(nombre="Sandwich de Queso Crema, Lacón y Huevos", descripcion="Queso crema, lacón braseado y huevos revueltos", precio=6.10, categoria="Nuestras Tostas"),

            # BAGELS
            Producto(nombre="Bagel de Queso Crema, Aguacate y Jamón", descripcion="Queso crema, aguacate, jamón cocido, tomate y rúcula", precio=7.80, categoria="Bagels"),
            Producto(nombre="Bagel de Tomate y Paleta Ibérica", descripcion="Tomate rallado con paleta ibérica y AOVE", precio=7.80, categoria="Bagels"),
            Producto(nombre="Bagel Vegano", descripcion="Hummus, tomate salteado y aguacate", precio=7.80, categoria="Bagels"),
            Producto(nombre="Galibagel", descripcion="Lacón braseado, queso de Arzúa y tomate", precio=7.80, categoria="Bagels"),
            Producto(nombre="Bagel Diversum", descripcion="Base de mozzarella, vinagre balsámico, fruta de temporada, bacon crujiente y rúcula", precio=7.80, categoria="Bagels"),

            # CROISSANTS / FRENCH TOAST / TORTITAS
            Producto(nombre="Croissant", descripcion="Auténtico croissant francés de mantequilla", precio=2.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Croissant a la Plancha", descripcion="Croissant francés a la plancha", precio=2.10, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Croissant con Mermelada y Mantequilla", descripcion="Croissant con mermelada casera y mantequilla", precio=3.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Croissant con Nocciola", descripcion="Croissant relleno de nocciola", precio=2.50, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Croissant con Jamón y Queso", descripcion="Croissant relleno de jamón y queso", precio=3.75, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Croissant Caprese", descripcion="Tomate en rodajas con mozzarella, rúcula y salsa pesto", precio=5.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="New York Roll", descripcion="Relleno y cobertura a elegir: Ganache de chocolate, Crema de mascarpone y nata, o Crema Lotus", precio=5.20, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="French Toast Tiramisú", descripcion="Con crema de queso mascarpone y nata, cacao en polvo", precio=7.50, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="French Toast de Fruta", descripcion="Fruta de temporada y coulis de mango", precio=7.50, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="French Toast Nocciola", descripcion="Nocciola y piña caramelizada", precio=7.50, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="3 Tortitas con Sirope", descripcion="Nuestra masa especial de tortitas americanas con sirope", precio=4.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Tortitas Nocciola y Frutas", descripcion="Nocciola, frutas y coulis de frutos rojos", precio=6.20, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Tortitas de Queso Mascarpone", descripcion="Queso mascarpone y frutas", precio=6.20, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Tortita XL Vegetal", descripcion="Queso crema, aguacate, tomate, piña y granada", precio=6.20, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Tortita XL Gallega", descripcion="Lacón, aceite, pimentón y queso de Arzúa", precio=6.20, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Tortitacos", descripcion="2 tortitas rellenas de huevo revuelto con bacon y queso, aguacate y pico de gallo", precio=7.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="Huerto y Corral", descripcion="Mix de salado (huevo revuelto, bacon y tomate) y dulce (nocciola, mermelada casera, mascarpone y frutas)", precio=7.00, categoria="Croissants/French Toast/Tortitas"),
            Producto(nombre="3 Tortitas con Huevos, Bacon y Cherries", descripcion="3 tortitas con huevos revueltos, bacon y cherries salteados", precio=6.90, categoria="Croissants/French Toast/Tortitas"),

            # FRUTAS NATURALES
            Producto(nombre="Zumo de Naranja", descripcion="Zumo de naranja natural", precio=2.80, categoria="Frutas Naturales"),
            Producto(nombre="Limonada Casera", descripcion="Limonada casera refrescante", precio=2.40, categoria="Frutas Naturales"),
            Producto(nombre="Smoothie Sunshine Power", descripcion="Naranja, zanahoria, mango y limón", precio=5.25, categoria="Frutas Naturales"),
            Producto(nombre="Smoothie Funny Berries", descripcion="Fresa, mora y frambuesa", precio=5.25, categoria="Frutas Naturales"),
            Producto(nombre="Smoothie Yellow Slow", descripcion="Piña, papaya y mango", precio=5.25, categoria="Frutas Naturales"),
            Producto(nombre="Bowl de Fruta de Temporada", descripcion="Fruta fresca de temporada", precio=5.25, categoria="Frutas Naturales"),
            Producto(nombre="Bowl de Yogur con Granola", descripcion="Yogur (o yogur vegetal) con frutas y granola casera", precio=6.00, categoria="Frutas Naturales"),

            # MENÚS DESAYUNOS
            Producto(nombre="Menú Serendipia", descripcion="Tortitas de nocciola, frutas y coulis + Media tosta de aguacate y tomate + Café grande + Zumo naranja o limonada", precio=12.50, categoria="Menús Desayunos"),
            Producto(nombre="Menú Chegar e Encher", descripcion="Copa de yogur, frutas y granola + Bagel a escoger + Café grande + Zumo naranja o limonada", precio=14.60, categoria="Menús Desayunos"),
            Producto(nombre="Menú Amodiño", descripcion="French toast de tiramisú + Media tosta de paleta ibérica y tomate + Café grande + Zumo naranja o limonada", precio=14.00, categoria="Menús Desayunos"),
            Producto(nombre="Mini Desayuno Croissant", descripcion="Café con leche grande y croissant con mantequilla y mermelada (De lunes a viernes hasta las 12:00)", precio=4.70, categoria="Menús Desayunos"),
            Producto(nombre="Mini Desayuno Tosta", descripcion="Café con leche grande y tosta de tomate y AOVE (De lunes a viernes hasta las 12:00)", precio=4.30, categoria="Menús Desayunos"),
            Producto(nombre="Pincho de Tortilla Española", descripcion="Pincho de tortilla española casera", precio=3.50, categoria="Menús Desayunos"),

            # CAPRICHOS DIVERSUM
            Producto(nombre="Galletas Diversum", descripcion="Chocolate, mantequilla con vainilla, avena con chocolate o veganas (con arándanos)", precio=0.60, categoria="Caprichos Diversum"),
            Producto(nombre="Muffins Diversum", descripcion="Chocolate, limón con semillas de amapola o veganos (con arándanos)", precio=2.20, categoria="Caprichos Diversum"),
            Producto(nombre="Bizcocho Tradicional o Chocolate", descripcion="Porción de bizcocho tradicional o de chocolate", precio=2.60, categoria="Caprichos Diversum"),
            Producto(nombre="Bizcocho de Limón o Naranja", descripcion="Limón con semillas de amapola o naranja con pepitas de chocolate", precio=2.80, categoria="Caprichos Diversum"),
            Producto(nombre="Minitartas Diversum", descripcion="Bizcochos con diferentes rellenos", precio=5.00, categoria="Caprichos Diversum"),
            Producto(nombre="Minitarta de Queso", descripcion="Minitarta de queso casera", precio=5.80, categoria="Caprichos Diversum"),
            Producto(nombre="Tartita de Ona", descripcion="Tartita de manzana caramelizada", precio=4.60, categoria="Caprichos Diversum"),
            Producto(nombre="Granola Diversum", descripcion="Elaborada en nuestra cocina (100 gr)", precio=2.00, categoria="Caprichos Diversum"),
            Producto(nombre="Brownie Sin Gluten", descripcion="Brownie de chocolate sin gluten", precio=2.80, categoria="Caprichos Diversum"),
            Producto(nombre="Muffin Sin Gluten", descripcion="Muffin de chocolate sin gluten", precio=2.50, categoria="Caprichos Diversum"),

            # CAFÉS / TÉS / CHOCOLATES / BEBIDAS
            Producto(nombre="Ristretto", descripcion="Café de especialidad Blend de Rober", precio=1.60, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Espresso", descripcion="Café de especialidad Blend de Rober", precio=1.60, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Café con Leche", descripcion="Café de especialidad con leche (normal)", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Café con Leche XL", descripcion="Café de especialidad con leche (XL)", precio=2.20, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Americano", descripcion="Café americano", precio=1.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cortado", descripcion="Café cortado", precio=1.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Latte Macchiato", descripcion="Latte macchiato (normal)", precio=1.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Latte Macchiato XL", descripcion="Latte macchiato (XL)", precio=2.00, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cappuccino", descripcion="Cappuccino con sirope opcional", precio=2.30, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cappuccino XL", descripcion="Cappuccino XL con sirope opcional", precio=2.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Café Lotus", descripcion="Café especial Lotus", precio=2.95, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Café Bombón", descripcion="Café bombón", precio=2.20, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Descafeinado Brasil", descripcion="Descafeinado especialidad Brasil con base de cacao y notas dulces", precio=1.60, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Leche Caliente", descripcion="Leche caliente", precio=1.30, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cola Cao o Nesquick Caliente", descripcion="Leche caliente con Cola Cao o Nesquick", precio=1.95, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Bati Cao", descripcion="Cola Cao o Nesquick con leche fría", precio=1.95, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Pink Latte", descripcion="Mezcla de leche de coco, granada, remolacha, cereza y jengibre", precio=2.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Chai Latte", descripcion="Cúrcuma, anís, cardamomo, jengibre y pimienta negra", precio=2.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cúrcuma Latte", descripcion="Leche Dorada con cúrcuma, canela, jengibre y pimienta negra", precio=2.70, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Poleo", descripcion="Té de poleo", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té de Frutos del Bosque", descripcion="Té de frutos del bosque", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Rooibos", descripcion="Té rooibos", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Negro Inglés", descripcion="Té negro inglés", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Negro con Leche", descripcion="Té negro inglés con leche", precio=1.95, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Verde", descripcion="Té verde", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Té Rojo", descripcion="Té rojo", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Tila", descripcion="Tila relajante", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Pócima Mágica", descripcion="Mezcla especial de hierbas", precio=2.00, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Manzanilla", descripcion="Manzanilla digestiva", precio=1.80, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Chocolate a la Taza Madagascar", descripcion="Bean to Bar - Notas de frambuesa, yogur, toffee y café", precio=2.90, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Chocolate a la Taza Tanzania", descripcion="Bean to Bar - Notas de frutas rojas, avellana y melaza", precio=2.90, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Agua", descripcion="Agua mineral", precio=1.40, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Agua con Gas", descripcion="Agua mineral con gas", precio=1.60, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Refrescos", descripcion="Coca-Cola, Fanta, Sprite, Aquarius", precio=2.20, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Zumos Naturales", descripcion="Zumos naturales variados", precio=2.50, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Cerveza Sin Alcohol", descripcion="Cerveza sin alcohol", precio=2.40, categoria="Cafés/Tés/Chocolates/Bebidas"),
            Producto(nombre="Kombucha", descripcion="Bebida fermentada probiótica", precio=3.50, categoria="Cafés/Tés/Chocolates/Bebidas"),
        ]
        
        for producto in productos_diversum:
            db.session.add(producto)
        
        db.session.commit()
        print("Base de datos inicializada con productos de Diversum")

# Ruta para servir el frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        static_folder_path = app.static_folder
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

