from flask import Blueprint, jsonify, request
from .models import Quote, db
import random

# Create a blueprint for the routes
main = Blueprint('main', __name__)

@main.route('/daily-quote', methods=['GET'])
def get_daily_quote():
    quotes = Quote.query.all()
    if not quotes:
        return jsonify({"message": "No quotes available."}), 404
    random_quote = random.choice(quotes)
    return jsonify({"id": random_quote.id,"quote": random_quote.quote}), 200

@main.route('/quote', methods=['POST'])
def create_quote():
    data = request.get_json()
    if 'quote' not in data:
        return jsonify({"error": "Quote is required"}), 400
    new_quote = Quote(quote=data['quote'])
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({"message": "Quote added successfully"}), 201

@main.route('/quote/<int:id>', methods=['DELETE'])
def delete_quote(id):
    quote = Quote.query.get(id)
    if not quote:
        return jsonify({"error": "Quote not found"}), 404
    db.session.delete(quote)
    db.session.commit()
    return jsonify({"message": "Quote deleted successfully"}), 200