import cognitive_face as CF

# Setting up keys and endpoint
KEY = '07afcfc6281347698f601d41e59a5afc'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

print KEY

r = CF.person_group.lists()
print r