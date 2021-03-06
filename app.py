## Nama : Aditiya Prayogy  (19090096) 6B
##        Dimas Ardiansyah ( 19090109) 6B
##Link Android  : https://github.com/aditiya2231/UasMobile6B

import os
import sys
import numpy as np
from util import base64_to_pil
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file


app = Flask(__name__)

model = load_model('mask_resnet50.h5') 

def model_predict(img, model):
    img = img.resize((150, 150))       
    
    x = image.img_to_array(img)
    
    x = np.expand_dims(x, axis = 0 )
    x = x.astype('float32')
    x = x / 255.0
    preds = model.predict(x)
    return preds

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)

        hasil_label = target_names[np.argmax(preds)]
        hasil_prob = "{:.2f}".format(100 * np.max(preds))

        return jsonify(result=hasil_label, probability=hasil_prob)

    return None

if __name__ == '__main__':
    app.run(debug=True)