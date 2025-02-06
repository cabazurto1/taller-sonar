#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Definir constantes
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
NOT_FOUND_MESSAGE = "Registro no encontrado"
ERROR_MESSAGE = "error"

# Configuración de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para toda la aplicación
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Obtener las variables de entorno para la base de datos
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelo para el Inventario
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_descargo = db.Column(db.DateTime, nullable=True)
    usuario_responsable = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'producto': self.producto,
            'cantidad': self.cantidad,
            'fecha_ingreso': self.fecha_ingreso.strftime(DATE_FORMAT) if self.fecha_ingreso else None,
            'fecha_descargo': self.fecha_descargo.strftime(DATE_FORMAT) if self.fecha_descargo else None,
            'usuario_responsable': self.usuario_responsable
        }

# Crear las tablas (si no existen)
with app.app_context():
    db.create_all()

# -----------------------------------------------------------
# Endpoints para la gestión del inventario
# -----------------------------------------------------------

# Obtener todos los registros del inventario
@app.route('/inventory', methods=['GET'])
def get_inventory():
    items = Inventory.query.all()
    return jsonify([item.to_dict() for item in items])

# Obtener un registro del inventario por ID
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    else:
        return jsonify({'message': NOT_FOUND_MESSAGE}), 404

# Crear un nuevo registro en el inventario
@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    try:
        nuevo_item = Inventory(
            producto=data['producto'],
            cantidad=data['cantidad'],
            fecha_ingreso=datetime.utcnow(),  # Se asigna la fecha de ingreso actual
            fecha_descargo=datetime.strptime(data['fecha_descargo'], DATE_FORMAT) if 'fecha_descargo' in data and data['fecha_descargo'] else None,
            usuario_responsable=data['usuario_responsable']
        )
        db.session.add(nuevo_item)
        db.session.commit()
        return jsonify(nuevo_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Actualizar un registro del inventario
@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    data = request.get_json()
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({'message': NOT_FOUND_MESSAGE}), 404
    try:
        if 'producto' in data:
            item.producto = data['producto']
        if 'cantidad' in data:
            item.cantidad = data['cantidad']
        if 'fecha_descargo' in data:
            item.fecha_descargo = datetime.strptime(data['fecha_descargo'], DATE_FORMAT) if data['fecha_descargo'] else None
        if 'usuario_responsable' in data:
            item.usuario_responsable = data['usuario_responsable']
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Eliminar un registro del inventario
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({'message': NOT_FOUND_MESSAGE}), 404
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Registro eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# -----------------------------------------------------------
# Iniciar la aplicación
# -----------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
