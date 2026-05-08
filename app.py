from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# 🌸 Catálogo de flores
flores = [
    {"id": 1, "nombre": "Rosa", "precio": 500},
    {"id": 2, "nombre": "Tulipán", "precio": 300},
    {"id": 3, "nombre": "Girasol", "precio": 400},
    {"id": 4, "nombre": "Orquídea", "precio": 800}
]

carrito = {}

# 🌼 Obtener todas las flores
@app.route('/flores', methods=['GET'])
def obtener_flores():
    """
    Obtener lista de flores
    ---
    responses:
      200:
        description: Lista de flores
    """
    return jsonify(flores)


# ➕ Agregar al carrito
@app.route('/carrito/agregar', methods=['POST'])
def agregar_carrito():
    """
    Agregar producto al carrito
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
    responses:
      200:
        description: Producto agregado
      404:
        description: Flor no encontrada
    """
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"error": "Falta el id"}), 400

    id_flor = data.get('id')

    if not any(f["id"] == id_flor for f in flores):
        return jsonify({"error": "Flor no encontrada"}), 404

    carrito[id_flor] = carrito.get(id_flor, 0) + 1

    return jsonify({"mensaje": "Producto agregado", "carrito": carrito})


# ➖ Restar del carrito
@app.route('/carrito/restar', methods=['POST'])
def restar_carrito():
    """
    Restar producto del carrito
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
    responses:
      200:
        description: Producto restado
    """
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"error": "Falta el id"}), 400

    id_flor = data.get('id')

    if id_flor not in carrito:
        return jsonify({"error": "No está en el carrito"}), 404

    carrito[id_flor] -= 1

    if carrito[id_flor] <= 0:
        del carrito[id_flor]

    return jsonify({"mensaje": "Producto restado", "carrito": carrito})


# 🛒 Ver carrito
@app.route('/carrito', methods=['GET'])
def ver_carrito():
    """
    Ver carrito
    ---
    responses:
      200:
        description: Lista de productos en carrito
    """
    resultado = []
    total = 0

    for id_flor, cantidad in carrito.items():
        flor = next((f for f in flores if f["id"] == id_flor), None)
        if flor:
            subtotal = flor["precio"] * cantidad
            total += subtotal
            resultado.append({
                "nombre": flor["nombre"],
                "cantidad": cantidad,
                "precio_unitario": flor["precio"],
                "subtotal": subtotal
            })

    return jsonify({"productos": resultado, "total": total})


# 🧹 Vaciar carrito
@app.route('/carrito/vaciar', methods=['DELETE'])
def vaciar_carrito():
    """
    Vaciar carrito
    ---
    responses:
      200:
        description: Carrito vaciado
    """
    carrito.clear()
    return jsonify({"mensaje": "Carrito vaciado"})


if __name__ == '__main__':
    app.run(debug=True)