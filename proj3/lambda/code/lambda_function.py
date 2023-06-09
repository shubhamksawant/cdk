import boto3
import requests
from requests_aws4auth import AWS4Auth
import json

host = '' # domain endpoint with trailing /
region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def lambda_handler(event,contex):
        # Register repository

        path = '_snapshot/my-snapshot-repo-name' # the OpenSearch API endpoint
        url = host + path

        payload = {
        "type": "s3",
        "settings": {
            "bucket": "ossbkp2",
            "region": "us-west-2",
            "role_arn": "arn:aws:iam::276301730779:role/opensearch-snapshot-role"
        }
        }

        headers = {"Content-Type": "application/json"}

        r = requests.put(url, auth=awsauth, json=payload, headers=headers)

        print(r.status_code)
        print(r.text)

        # # Take snapshot
        #
        path = '_snapshot/my-snapshot-repo-name/my-snapshot'
        url = host + path

        r = requests.put(url, auth=awsauth)

        print(r.text)

        

