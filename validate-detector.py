##########################################################
# the-heart-of-gold/matroid-scripts/validate-detector.py #
# 05/10/2021                                             #
##########################################################

import sys
import os
import fnmatch
import requests
import logging
import matroid
from matroid.client import Matroid
import json
import pandas as pd


class CONSTANTS:
    '''
    A class to hold some API and other constants.
    '''
    MATROID_BASE_URL = 'https://matroid.nssif.gov.uk'
    #MATROID_BASE_URL = 'https://www.matroid.com'
    API_TIMEOUT = 5
    DETECTOR_ENDPOINT = '/api/v1/detectors'
    CARS_1225_DETECTOR_ID = '61b09bf34eccf955e5662d95'


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["authorization"] = f'Bearer {self.token}'
        return r


def get_detectors(access_token):
    print(f'{CONSTANTS.MATROID_BASE_URL}/api/v1/detectors')
    #response = requests.get(f'{base_url}/api/v1/detectors/', auth=BearerAuth(bearer_token), verify=False,)
    response = requests.get(
            f'{CONSTANTS.MATROID_BASE_URL}/api/v1/detectors/',
            headers={ 'Authorization': 'Bearer {}'.format(access_token) },
            timeout=5)
    return response


def classify_image(detector_id, image_path, access_token):
    '''
    param: detector_id: the ID # for the detector to use to classify the image
    param: image_path: the image file to be classified
    return: the JSON response from the detector
    '''
    files = {'file': open(image_path,'rb')}
    #files = {'file[]': [open(f'{test_data_dir}{image}','rb'),open(f'{test_data_dir}{image}','rb')]}
    print(f'{CONSTANTS.MATROID_BASE_URL}{CONSTANTS.DETECTOR_ENDPOINT}/{detector_id}/classify_image')
    response = requests.post(f'{CONSTANTS.MATROID_BASE_URL}{CONSTANTS.DETECTOR_ENDPOINT}/{detector_id}/classify_image',
            auth=BearerAuth(access_token),
            files=files,
            verify=False,
            )
    print(response.text)
    return response.json()


def main():
    assert(len(sys.argv) == 5), \
    'Usage: python validate-detetor.py [DETECTOR_ID] [VALIDATION_DATA_DIR] [OUTPUT_DIR] ["COMMA,SEPARATED,LABELS"]'
    detector_id = sys.argv[1]
    detector_endpoint = 'detectors/'+detector_id+'/'
    val_data_dir = sys.argv[2]+'/'
    output_dir = sys.argv[3]+'/'
    labels = sys.argv[4].split(',')
   
    # Load the bearer token
    with open('./secrets.txt','r') as f:
        access_token = f.read().rstrip('\n')

    # Matroid check (authentication and detector)
    try:
        print(f'reconstructed url: {CONSTANTS.MATROID_BASE_URL}/api/v1/detectors/{detector_id}')
        url = f'{CONSTANTS.MATROID_BASE_URL}/api/v1/detectors/{detector_id}'
        print(f'url: {url}')
        ret = requests.get(
        '{}/api/v1/detectors/{}'.format(CONSTANTS.MATROID_BASE_URL, detector_id),
        headers={ 'Authorization': 'Bearer {}'.format(access_token) },
        timeout=5)
    except requests.exceptions.Timeout:
        logging.error('Matroid check timeout.')
        raise
    except Exception as e:
        logging.error('Matroid check error.')
        raise
    if ret.status_code != 200:
        raise RuntimeError('Matroid check failed with access token "{}" and detector id "{}". \
                           HTTP status code {}.'.format(args.access_token, args.detector_id, ret.status_code))

    print(f'Response: {ret}')

    response = get_detectors(access_token)
    print(response)
    json_data = {}
    for file in os.listdir(val_data_dir):
        if fnmatch.fnmatch(file, '*.jpg'):
            # Classify each image using the given detector
            json_data[file] = classify_image(detector_id, os.path.join(val_data_dir, file), access_token)
            # Use the Matroid package API object to classify an image - DOESN'T WORK ATM :(
            #result = api.classify_image(detector_id=detector_id, image_file=f'{test_data_dir}{file}')
    
    # Write the json data to file.
    with open('validator_results.json', 'w') as f:
        json.dump(json_data, f, indent=4,)

'''
    with open('knife_test_results.json', 'r') as f:
        json_data = json.load(f)
    #df = pd.DataFrame.from_dict(json_data, orient='index')
    df = pd.DataFrame(columns=['image','prediction','bbox_left','bbox_top','bbox_width','bbox_height'],)
    for k,v in json_data.items():
        results = v['results'][0]
        print(results)
        if 'predictions' in results:
            print(results['file'])
            df.loc[len(df.index)] = [
                    results['file']['name'],
                    results['predictions'][0]['labels']['knife'],
                    results['predictions'][0]['bbox']['left'],
                    results['predictions'][0]['bbox']['top'],
                    results['predictions'][0]['bbox']['width'],
                    results['predictions'][0]['bbox']['height'],
                    ]
    print(df.head)
    print(df.columns)
    df.to_csv('knife_test_results.csv', header=True, index=False, encoding='utf-8',)
''' 


if __name__ == "__main__":
    main()

