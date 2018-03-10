#!flask/bin/python
import json

import requests
from flask import Flask
import cognitive_face as CF

# Setting up keys and endpoint
KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# Images
img_url = 'https://how-old.net/Images/faces2/main007.jpg'
img = open('how-old-img.jpg')
img1 = open('photo1.jpg')
img2 = open('photo2.jpg')

# Face id's
global ammarFaceId

person_group_id = 'man'
person_id = 'ammar'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/face/detect-url')
def detectUrl():
    r = CF.face.detect(img_url)
    return json.dumps(r)

@app.route('/face/detect-file')
def detectFile():
    r = CF.face.detect('photo1.jpg')
    _json = json.dumps(r)
    ammarFaceId = r[0]['faceId']
    print ammarFaceId
    return _json

@app.route('/face/identify/<faceId>')
def identify(faceId):
    r = CF.face.identify([faceId], person_group_id)
    return json.dumps(r)

if __name__ == '__main__':
    app.run(debug=True)
