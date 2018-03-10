#!flask/bin/python
import json

import requests
from flask import Flask
import cognitive_face as CF

KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

img_url = 'https://how-old.net/Images/faces2/main007.jpg'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/face/detect')
def detect():
    r = CF.face.detect(img_url)
    return json.dumps(r)

if __name__ == '__main__':
    app.run(debug=True)
