from flask import Blueprint, jsonify, request
from . import mongo
import random

# Create a blueprint for the routes
main = Blueprint('main', __name__)

@main.route('/daily-quote', methods=['GET'])
def get_daily_quote():
    quotes = list(mongo.db.quotes.find())
    if not quotes:
        return jsonify({"message": "No quotes available."}), 404
    random_quote = random.choice(quotes)
    return jsonify({"id": str(random_quote['_id']), "quote": random_quote['quote']}), 200

@main.route('/quote', methods=['POST'])
def create_quote():
    data = request.get_json()
    if 'quote' not in data:
        return jsonify({"error": "Quote is required"}), 400
    new_quote = {"quote": data['quote']}
    mongo.db.quotes.insert_one(new_quote)
    return jsonify({"message": "Quote added successfully"}), 201

@main.route('/quote/<id>', methods=['DELETE'])
def delete_quote(id):
    result = mongo.db.quotes.delete_one({"_id": mongo.db.ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Quote not found"}), 404
    return jsonify({"message": "Quote deleted successfully"}), 200
