import os
import json
import hashlib
import requests
from google.cloud import storage


class PageSpeedInsights:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.bucket = storage.Client().bucket(os.environ.get("BUCKET"))
        self.path_to_file = os.environ.get("PATH_TO_FILE")

    def run(self):
        params = {
            "key": self.api_key,
            "url": "https://vuanem.com",
            "strategy": "mobile",
        }
        with requests.get(
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed", params=params
        ) as r:
            results = r.json()
        results["lighthouseResult"].pop("audits")
        results["lighthouseResult"].pop("categoryGroups")
        results_str = json.dumps(results)
        blob = self.bucket.blob(
            self.path_to_file + hashlib.sha1(results_str.encode()).hexdigest() + ".json"
        )
        blob.upload_from_string(results_str)


def main(request):
    job = PageSpeedInsights()
    job.run()
    return "ok"
