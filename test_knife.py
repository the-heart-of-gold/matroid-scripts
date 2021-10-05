###################################################
# the-heart-of-gold/matroid-scripts/test_knife.py #
# 05/10/2021                                      #
###################################################

import os
import fnmatch
import json
import requests
import matroid
from matroid.client import Matroid


#api = Matroid(client_id='XXXXX', client_secret='XXXXXXXXXXX')
#api = Matroid(base_url='http://www.matroid.com/api/v1/',
#        client_id='',
#        client_secret=''
#        )

base_url = 'https://www.matroid.com/api/v1/'
bearer_token = 'YOUR-TOKEN-HERE'
detector_endpoint = 'detectors/XXX/'
detector_id = 'XXX'
headers = {'Authorization': f'{bearer_token}'}
test_data_dir = '/your/data/path/to/test/images/'


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["authorization"] = f'Bearer {self.token}'
        return r


def get_detectors():
    response = requests.get(f'{base_url}detectors', auth=BearerAuth(bearer_token), verify=False,)


def classify_image(image):
    files = {'file': open(f'{test_data_dir}{image}','rb')}
    #files = {'file[]': [open(f'{test_data_dir}{image}','rb'),open(f'{test_data_dir}{image}','rb')]}
    response = requests.post(f'{base_url}{detector_endpoint}classify_image',
            auth=BearerAuth(bearer_token),
            files=files,
            verify=False,
            )
    print(response.url)
    print(response.json())
    return response.json()


def main():
    # Use the Matroid package to access the account info through the api object
    #info = api.account_info()
    #print(info)
    
    #get_detectors()
    json_data = {}
    for file in os.listdir(test_data_dir):
        if fnmatch.fnmatch(file, '*.jpg'):
            print(file)
            json_row = classify_image(file)
            print(json_row)
            # Use the Matroid package API object to classify an image - DOESN'T WORK ATM :(
            #result = api.classify_image(detector_id=detector_id, image_file=f'{test_data_dir}{file}')


if __name__ == "__main__":
    main()

