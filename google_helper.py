import datetime
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build


def create_service(service_account_secret_file, api_name, api_version):
    print(service_account_secret_file, api_name, api_version, sep='-')
    SERVICE_ACCOUNT_FILE = service_account_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    service_account_info = json.load(open(SERVICE_ACCOUNT_FILE))
    cred = service_account.Credentials.from_service_account_info(
        service_account_info)


    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
