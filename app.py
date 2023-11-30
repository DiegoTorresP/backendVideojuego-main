from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from waitress import serve

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://unity:unity@cluster0.kczqgdb.mongodb.net/unity?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/top_scores/<int:level>', methods=['GET'])
def get_top_scores(level):
    collection = mongo.db.player
    top_scores = collection.find({}, {"_id": 0, f"Level{level}": 1, "Name":1}).sort(f"Level{level}", -1).limit(3)
    return jsonify(list(top_scores))


@app.route('/save_score', methods=['POST'])  
def save_score():
    data = request.get_json()
    name = data['name']
    score = data['score']
    level = data['level']
    
    filter = {"Name": name}
    update = {"$set": {f"Level{level}": score}}
    
    mongo.db.player.update_one(filter, update, True)

    return jsonify({"result": "Score saved"})

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080) 

