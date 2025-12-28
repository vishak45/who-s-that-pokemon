import base64
import io
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import json

with open("class_labels.json") as f:
    class_indices = json.load(f)

class_labels = {v: k for k, v in class_indices.items()}

from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

model = load_model("pokemon_classifier.keras")

@app.route('/guess', methods=['POST'])
def guess_pokemon():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    
    image_base64 = data['image']
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    
    image = image.resize((128, 128))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    
    prediction = model.predict(image_array)

    predicted_index = int(np.argmax(prediction[0]))
    confidence = float(prediction[0][predicted_index])
    preds = prediction[0]
    list=[]
    top3 = preds.argsort()[-3:][::-1]
    for i in top3:
        list.append(class_labels[i])

    predicted_class = class_labels[predicted_index]
    print(f"Predicted class: {predicted_class}, Confidence: {confidence * 100}%")
    return jsonify({
        "name": predicted_class,
        "confidence": confidence * 100,
        "top3": list
    })


  


if __name__ == "__main__":
    app.run(debug=True)