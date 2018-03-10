#!flask/bin/python
import json

import requests
from flask import Flask, request, Response
import cognitive_face as CF

# Setting up keys and endpoint
KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

person_group_id = 'hack24_peeps'

app = Flask(__name__)

def getFaceId(img):
    res = CF.face.detect(img)
    return res[0]['faceId']

def matchFace(faceId):
    res = CF.face.identify([faceId], person_group_id)
    return res[0]['candidates'][0]

def getPerson(personId):
    res = CF.person.get(person_group_id, personId)
    return res

def createNewPerson(img, name):
    res = CF.person.create(person_group_id, name)
    personId = res['personId']
    CF.person.add_face(img, person_group_id, personId)
    CF.person_group.train(person_group_id)

# Registering a new person
@app.route('/register/<name>', methods=['POST'])
def register(name):
    f = request.files['file']
    f.save('uploaded_img.jpg')
    createNewPerson('uploaded_img.jpg', name)
    return Response(status=201)

# Identifying against an existing person
@app.route('/identify', methods=['POST'])
def identify():
    f = request.files['file']
    f.save('uploaded_img.jpg')
    faceId = getFaceId('uploaded_img.jpg')
    faceMatch = matchFace(faceId)
    personId  = faceMatch['personId']
    person = getPerson(personId)
    return json.dumps(person)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
