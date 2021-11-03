'''
 the-heart-of-gold/matroid-scripts/classify_images.py
 Date: 05/10/202
 Author: Dave Dyke

 CLI script that takes a label, a classification detector
 ID, and a/path/to/test/images. The output is json written
 to file detailing successful/failed classifications. 
                                                           
'''

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
headers = {'Authorization': f'{bearer_token}'}


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["authorization"] = f'Bearer {self.token}'
        return r


def get_detectors():
    response = requests.get(f'{base_url}detectors', auth=BearerAuth(bearer_token), verify=False,)


def classify_image(detector_id, image):
    files = {'file': open(f'{test_data_dir}{image}','rb')}
    #files = {'file[]': [open(f'{test_data_dir}{image}','rb'),open(f'{test_data_dir}{image}','rb')]}
    response = requests.post(f'{base_url}detectors/{detector_id}/classify_image',
            auth=BearerAuth(bearer_token),
            files=files,
            verify=False,
            )
    return response.json()


def main():
    assert(len(sys.argv) == 5), \
            'Usage: python classify_images.py [IMAGE_DIR] [DETECTOR_ID] [LABEL] [OUTPUT_FILE]'
    image_dir = sys.argv[1]+'/'
    detector_id = argv[2]
    label = sys.argv[3]
    output_file = argv[4]

    assert(os.path.exists(image_dir)), \
            f'Image directory {image_dir} does not exist.'

    ##
    ## Part 1: Generate positive sample for each label ##
    ##

    ##Use the Matroid package to access the account info through the api object
    #info = api.account_info()
    #print(info)
    
    #get_detectors()
    json_data = {}
    for file in os.listdir(image_dir):
        if fnmatch.fnmatch(file, '*.jpg'):
            print(file)
            json_item = classify_image(dectector_id, file)
            json_data[file] = json_item
            # Use the Matroid package API object to classify an image - DOESN'T WORK ATM :(
            #result = api.classify_image(detector_id=detector_id, image_file=f'{test_data_dir}{file}')
    with open(output_file, 'w') as of:
        json.dump(of, indent=4)


if __name__ == "__main__":
    main()

