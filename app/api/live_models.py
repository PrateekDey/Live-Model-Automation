import boto3
import requests
from http import HTTPStatus

from app.api.pynamodb_models import get_live_model_tables
from app.api.sisense_endpoints import get_endpoint
from app.api.table_handle import get_recent_connections
from app.setup_structlog import get_logger
from app import arguments

_logger = get_logger(arguments.PROGRAM_NAME)


def create_live_cube(parameter: dict):
    _logger.info('Creating live cube on LocalHost', Live_cube=parameter['datamodel_name'])
    endpoint, headers = get_endpoint('create_live_cube')
    data = {
        "title": parameter.get('datamodel_name'),
        "type": "live"
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    _logger.info('Successfully created live cube on LocalHost')
    return response


def create_live_dataset(parameter: dict):
    _logger.info('Creating datasets for Live cube', Live_oid=parameter.get('datamodel_oid'))
    endpoint, headers = get_endpoint('create_live_dataset', parameter.get('datamodel_oid'))
    data = {
        "name": parameter.get('dataset_name'),
        "type": "live",
        "connection": {
            "provider": parameter.get('provider'),
            "parameters": {
                "ApiVersion": "2",
                "Server": parameter.get('server'),
                "UserName": parameter.get('username'),
                "Password": parameter.get('password'),
                "DefaultDatabase": parameter.get('defaultdatabase'),
                "EncryptConnection": "true",
                "TrustServerCertificate": "true",
                "AdditionalParameters": "",
                "Database": parameter.get('database')
            },
            "schema": parameter.get('schema'),
            "timeout": 300000,
            "refreshRate": 600000,
            "resultLimit": 50000,
            "uiParams": {},
            "globalTableConfigOptions": {}
        }
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    if response.status_code != HTTPStatus.CREATED:
        raise Exception("Wrong credentials", response.json())
    _logger.info(f"Successfully added dataset to the datamodel {parameter['datamodel_name']}")
    return response


def add_table(parameter: dict, table_name: str, table_id: str, column_list: list, query: str):
    _logger.info(f'Adding table {table_name}')
    endpoint, headers = get_endpoint('create_live_table', parameter['datamodel_oid'], parameter['dataset_oid'])
    data = {
        "id": table_id,
        "name": table_name,
        "columns": column_list,
        "buildBehavior": {
            "type": "sync",
            "accumulativeConfig": None
        },
        "hidden": False,
        "description": None,
        "configOptions": {
            "importQuery": query
        }
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    _logger.info(f"{table_name} added")
    return response.json()


def get_dynamodb_table(table_schema: str):
    client = boto3.client('dynamodb', region_name=arguments.aws_region)
    table_name = "live-model-table-structure"
    key = "table_schema"

    response = client.get_item(Key={
        key: {
            "S": table_schema
        }
    }, TableName=table_name)


# creates a basic datamodel with a dataset
def get_basic_model(parameter: dict):
    parameter['datamodel_oid'] = create_live_cube(parameter).json()['oid']
    parameter['dataset_oid'] = create_live_dataset(parameter).json()['oid']
    parameter['conn_oid'] = get_recent_connections().get('oid')

    table_record = get_live_model_tables(parameter.get('table_choice'))
    return table_record


def publish_model(parameter: dict):
    _logger.info(f"Publishing the Model {parameter['datamodel_name']}")
    endpoint, headers = get_endpoint('ecm')
    data = {
        "query": "mutation publishElasticube($elasticubeOid: UUID!) \
        {\n  publishElasticube(elasticubeOid: $elasticubeOid)\n}\n",
        "variables": {
            "elasticubeOid": parameter['datamodel_oid']
        },
        "operationName": "publishElasticube"
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.status_code
