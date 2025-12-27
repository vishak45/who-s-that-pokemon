import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/guess', methods=['POST'])
def guess_pokemon():
    data = request.get_json()
    image_data = data['image']
    # process the image data and return the predicted pokemon name