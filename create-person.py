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

# Setting up person group
person_group_id = 'man'
name = 'ammar'
# CF.person_group.create(person_group_id)
res = CF.person.create(person_group_id, name)
person_id = res['personId']
CF.person.add_face('photo3.jpg', person_group_id, person_id)
CF.person_group.train(person_group_id)
