#!flask/bin/python
import json

import requests
from flask import Flask, request
import cognitive_face as CF

# Setting up keys and endpoint
KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# Images
# img_url = 'https://how-old.net/Images/faces2/main007.jpg'
# img = open('how-old-img.jpg')

# Face id's
# global ammarFaceId

person_group_id = 'man'
person_id = 'ammar'

app = Flask(__name__)

def getFaceId(img):
    res = CF.face.detect(img)
    return res[0]['faceId']

def matchFace(faceId):
    res = CF.face.identify([faceId], person_group_id)
    return len(res[0]['candidates']) > 0

def createNewPerson(img, name):
    res = CF.person.create(person_group_id, name)
    personId = res['personId']
    CF.person.add_face(img, person_group_id, personId)

@app.route('/register/<name>')
def register(name):
    f = request.file['file']
    f.save('uploaded_img.jpg')
    createNewPerson('uplodaded_img.jpg', name)

@app.route('/identify')
def identify():
    f = request.file['file']
    f.save('uploaded_img.jpg')
    faceId = getFaceId('uploaded_img.jpg')
    faceMatchExists = matchFace(faceId)
    return faceMatchExists

# @app.route('/face/detect-url')
# def detectUrl():
#     r = CF.face.detect(img_url)
#     return json.dumps(r)

# @app.route('/face/detect-file')
# def detectFile():
#     r = CF.face.detect('daniel.jpg')
#     r2 = CF.face.detect('photo1.jpg')
#     _json = json.dumps(r)
#     ammarFaceId = r[0]['faceId']
#     return _json + json.dumps(r2)

# @app.route('/face/identify/<faceId>')
# def faceIdentify(faceId):
#     r = CF.face.identify([faceId], person_group_id)
#     print len(r[0]['candidates'])
#     return json.dumps(r)

if __name__ == '__main__':
    app.run(debug=True)
