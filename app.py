#!flask/bin/python
import json
import os.path
import requests
from flask import Flask, request, Response
import cognitive_face as CF

# Setting up keys and endpoint
VISION_API_KEY = '268f4aaa48a3465b8b8492c1532b798d'
VISION_API_BASE = 'https://westeurope.api.cognitive.microsoft.com/vision/v1.0/'
FACE_API_KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(FACE_API_KEY)
FACE_API_BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(FACE_API_BASE_URL)
WEBSERVICES_BASE = "http://51.143.186.87:8080"

person_group_id = 'hack24_peeps'

app = Flask(__name__)

def getFaceId(img):
    res = CF.face.detect(img)
    return res[0]['faceId']

def matchFace(faceId):
    res = CF.face.identify([faceId], person_group_id)
    candidates = res[0]['candidates']
    if len(candidates) > 0:
        return candidates[0]
    else:
        return None

def getPerson(personId):
    res = CF.person.get(person_group_id, personId)
    return res

def createNewPerson(img, name):
    res = CF.person.create(person_group_id, name)
    personId = res['personId']
    CF.person.add_face(img, person_group_id, personId)
    CF.person_group.train(person_group_id)

def parse_image(image):
    if hasattr(image, 'read'):  # When image is a file-like object.
        headers = {'Content-Type': 'application/octet-stream'}
        data = image.read()
        return headers, data, None
    elif os.path.isfile(image):  # When image is a file path.
        headers = {'Content-Type': 'application/octet-stream'}
        data = open(image, 'rb').read()
        return headers, data, None
    else:  # Default treat it as a URL (string).
        headers = {'Content-Type': 'application/json'}
        json = {'url': image}
        return headers, None, json

def record_location(personid,location):
    url = WEBSERVICES_BASE + "/appearance/" + personid
    body = location
    resp = requests.put(url,data=body)
    return resp

# Get objects from vision API
def getObjects():
    vision_description_url = VISION_API_BASE + 'describe'
    headers, data, json = parse_image('uploaded_img.jpg')
    headers['Ocp-Apim-Subscription-Key'] = VISION_API_KEY
    response = requests.post(vision_description_url, headers=headers, data=data, json=json)
    return response.json()

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
    location = request.data['location']
    f.save('uploaded_img.jpg')
    objectsFlag = request.args.get('objects')
    # Check for objects flag and ping vision api if set to true
    faceId = getFaceId('uploaded_img.jpg')
    faceMatch = matchFace(faceId)
    if faceMatch is not None:
        personId  = faceMatch['personId']
        location_resp = record_location(personId, location)
        person = getPerson(personId)
        if objectsFlag is not None:
            visionDict = getObjects()
            result = { key: value for (key, value) in (visionDict.items() + person.items()) }
            return json.dumps(result)
        else:
            return json.dumps(person)
    else:
        return Response(status=404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
