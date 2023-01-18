import boto3
import unittest
import app.api.live_models
from moto import mock_ssm
from requests import Response
from mock import patch


@mock_ssm
def setup():
    client = boto3.client("ssm", region_name="us-east-1")
    client.put_parameter(
        Name="insights_data_admin_token", Description="test token parameter", Value='{"token": "testToken"}',
        Type="SecureString"
    )
    client.put_parameter(
        Name="insights_admin_token", Description="test token parameter", Value='{"token": "testToken"}',
        Type="SecureString"
    )


some_dict = {
    'datamodel_name': 'sample_data_model',
    'dataset_name': 'sample_dataset',
    'datamodel_oid': 'sample_datamodel_oid',
    'dataset_oid': 'sample_dataset_oid',
    'server': 'someserver',
    'username': 'test_user',
    'password': 'password',
    'defaultdatabase': 'defaultdb',
    'database': 'db',
    'provider': "RedShift",
    'schema': 'schema_name'
}


class UnitTestClass(unittest.TestCase):
    @mock_ssm
    def test_create_live_cube(self):
        setup()
        resp = Response()
        resp.status_code = 200
        resp._content = {
            "oid": "some_datamodel_oid",
            "title": "test_live_cube",
            "server": "LocalHost",
            "serverId": "some_server_id",
            "type": "live",
            "creator": {
                "id": "some_creator_id",
                "userName": "test_user",
                "email": "sampleEmail@syncron.com",
            },
            "tenant": {
                "_id": "some_tenant_id",
                "name": "system"
            }

        }

        with patch('requests.post', return_value=resp):
            assert app.api.live_models.create_live_cube(some_dict).status_code == 200

    @mock_ssm
    def test_create_live_dataset(self):
        setup()
        resp = Response()
        resp.status_code = 201
        resp._content = {
            "oid": "some_dataset_oid",
            "type": "live",
            "owner": {
                "id": "some_creator_id",
                "userName": "test_user",
                "email": "sampleEmail@syncron.com",
            },
            "connection": {
                "id": "some_id",
                "oid": "some_datamodel_oid",
                "owner": {
                    "id": "owner_id",
                    "userName": "test_user1",
                    "email": "testEmail@syncron.com",
                },
                "provider": "RedShift",
                "parameters": {
                    "ApiVersion": "2",
                    "Server": "some_server",
                    "UserName": "user1",
                    "Password": "password",
                    "DefaultDatabase": "defaultdb",
                    "Database": "db"
                },
                "schema": "schema_name",
                "timeout": 300000,
                "refreshRate": 600000,
                "resultLimit": 50000,
                "protectedParameters": [
                    "Password"
                ]
            },
            "name": "sample_dataset"
        }
        with patch('requests.post', return_value=resp):
            assert app.api.live_models.create_live_dataset(some_dict).status_code == 201


if __name__ == '__main__':
    unittest.main()
