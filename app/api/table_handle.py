import requests
from app import arguments
from app.api.sisense_endpoints import get_endpoint
from app.setup_structlog import get_logger

_logger = get_logger(arguments.PROGRAM_NAME)


def get_recent_connections():
    _logger.info("Fetching the recent connection")
    endpoint, headers = get_endpoint('connections')
    response = requests.get(url=endpoint, headers=headers)
    return response.json()[-1]


def table_schema_data(parameter: dict, table_name: str, query: str):
    _logger.info('Fetching details of the table')

    endpoint, headers = get_endpoint('table_schema_details', parameter['conn_oid'])
    data = {
        "provider": parameter.get('provider'),
        "connectionData": {
            "connection": {
                "ApiVersion": "2",
                "Server": parameter.get('server'),
                "UserName": parameter.get('username'),
                "DefaultDatabase": parameter.get('defaultdatabase'),
                "EncryptConnection": "false",
                "UseDynamicSchema": "false",
                "AdditionalParameters": "",
                "Database": parameter.get('database'),
                "importQuery": query
            },
            "schema": parameter.get('schema'),
            "table": table_name,
            "fetchRelations": "true"
        }
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def orient_columns(column_list: list):
    new_column_list = list()
    for column in column_list:
        ex = {
            "id": column["columnName"],
            "name": column['columnName'],
            "type": column['dbType'],
            "size": column['size'],
            "precision": column['precision'],
            "scale": column['scale'],
            "hidden": False
        }
        new_column_list.append(ex)
    return new_column_list


def add_relation(parameter: dict, main_table: str, col_id_from_main: str, second_table: str):
    _logger.info(f"Adding relations to {main_table} -> {second_table}")
    endpoint, headers = get_endpoint('create_relation', parameter['datamodel_oid'])
    data = {
        "columns": [{
            "dataset": parameter['dataset_oid'],
            "table": parameter['table_list'][main_table]['table oid'],
            "column": col_id_from_main
        }, {
            "dataset": parameter['dataset_oid'],
            "table": parameter['table_list'][second_table]['table oid'],
            "column": parameter['table_list'][second_table][parameter['table_list'][second_table]['id']]
        }]
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
