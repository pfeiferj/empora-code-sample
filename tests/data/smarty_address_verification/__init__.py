import json
import os
from sample.models.settings import settings

dir_path = os.path.dirname(os.path.realpath(__file__))


def successful_response_data():
    with open(f"{dir_path}/successful_response.json") as f:
        return json.load(f)

def successful_response_data_1():
    with open(f"{dir_path}/successful_response_1.json") as f:
        return json.load(f)


def mock_successful_response(mock):
    data = successful_response_data()
    mock.post(f"{settings.smarty_api_base_route}/street-address", json=data)

