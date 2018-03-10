import cognitive_face as CF

# Setting up keys and endpoint
KEY = '030d5c89e600472bba1d148dddcff568'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# Setting up person group
person_group_id = 'hack24_peeps'

CF.person_group.delete(person_group_id)
