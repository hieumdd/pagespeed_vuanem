import os
import json
import hashlib
import requests
from google.cloud import storage

class PageSpeedInsights:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.bucket = storage.Client().bucket(os.environ.get('bucket'))
        self.path_to_file = os.environ.get('PATH_TO_FILE')
        
    def hash(self, data):
        hash_obj = hashlib.sha1(data.encode())
        return hash_obj.hexdigest()

    def test(self):
        params = {
            'key': self.api_key,
            'url': 'https://vuanem.com',
            'strategy': 'mobile'
        }
        with requests.get(
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed", params=params
        ) as r:
            blob = self.bucket.blob(self.path_to_file + hashlib.sha1(json.dumps(r.json()).encode()).hexdigest() + '.json')
            blob.upload_from_string(
                json.dumps(r.json())
            )          


if __name__ == "__main__":
    job = PageSpeedInsights()
    job.test()
