import os
import fnmatch
import requests


base_url = 'https://www.matroid.com/api/v1/'
detector_endpoint = 'detectors/61513042cfb3d60006002692/'
bearer_token = 'YOUR_ACCESS_TOKEN_HERE'
headers = {'Authorization': f'{bearer_token}'}
test_data_dir = '/data/dev/matroid-bbox/data/knife-detector/test/images/knife-small/'


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["authorization"] = f'Bearer {self.token}'
        return r


def get_detectors():
    response = requests.get(f'{base_url}detectors', auth=BearerAuth(bearer_token))


def classify_image(image):
    files = {'file': open(f'{test_data_dir}{image}','rb')}
    response = requests.post(f'{base_url}{detector_endpoint}classify_image',
            auth=BearerAuth(bearer_token),
            files=files,
            verify=True,
            )


def main():
    get_detectors()
    for file in os.listdir(test_data_dir):
        if fnmatch.fnmatch(file, '*.jpg'):
            print(file)
            classify_image(file)


if __name__ == "__main__":
    main()

