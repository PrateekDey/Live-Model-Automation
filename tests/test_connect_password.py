import requests
import unittest
from unittest import mock


# This is the class we want to test
class DoRESTRequests:
    @staticmethod
    def fetch_json(url):
        response = requests.get(url)
        return response.json()


pid = 12345
password_url = "https://passwords.syncron.team"
expected_response = {
    'server': 'someserver',
    'username': 'user1',
    'password': 'password',
    'defaultdatabase': 'defaultdb',
    'database': 'db'
}
password_portal_endpoint= "{}/api/passwords/{}?QueryAll=true"


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == password_portal_endpoint.format(password_url, pid):
        return MockResponse(expected_response, 200)

    return MockResponse(None, 404)


class UnitTestClass(unittest.TestCase):
    @mock.patch('requests.get',
                side_effect=mocked_requests_get)  # side_effect: A function to be called whenever the Mock is called
    def test_get_password(self, mock_get):
        # Assert requests.get calls
        rest_call_obj = DoRESTRequests()
        json_data = rest_call_obj.fetch_json(password_portal_endpoint.format(password_url, pid))
        self.assertEqual(json_data, {
            'server': 'someserver',
            'username': 'user1',
            'password': 'password',
            'defaultdatabase': 'defaultdb',
            'database': 'db'
        })


if __name__ == '__main__':
    unittest.main()
