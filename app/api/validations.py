import requests

from app.api.pynamodb_models import get_datalake_tenants
from app.api.sisense_endpoints import get_endpoint
from app.setup_structlog import get_logger
from app import arguments


_logger = get_logger(arguments.PROGRAM_NAME)


def get_tenants(tenant_name: str):
    if get_datalake_tenants(tenant_name):
        return True


def get_model_list():
    model_list = []
    endpoints, headers = get_endpoint("model_list")
    response = requests.get(endpoints, headers=headers)
    for temp in response.json():
        if temp.get('type') == 'live':
            model_list.append(temp['title'])

    return model_list


def get_groups():
    groups = list(dict())
    url, headers = get_endpoint('groups_list')
    response = requests.get(url, headers=headers)
    for meta in response.json():
        groups.append({"name": meta.get('name'),
                       "id": meta.get('_id')})
    return groups


def add_model_to_group(datamodel_name: str, group_id: str, permission: str):
    _logger.info("Adding model to the group")
    url, headers = get_endpoint("add_model_to_group")
    data = {
        "server": "LocalHost",
        "elasticube": datamodel_name,
        "shares": [
            {
                "partyId": group_id,
                "type": "group",
                "permission": permission
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


def create_group(parameter: dict):
    _logger.info(f"Creating new group {parameter.get('datagroup_name')}")
    url, headers = get_endpoint("create_group")
    data = {
        "name": parameter.get('datagroup_name'),
        "excludeFromSharing": False
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    add_model_to_group(parameter.get('datamodel_oid'), response.json()['_id'], parameter.get('permission'))


def check_if_tenant_exists(tenant: str):
    if 'product' in tenant:
        return True
    elif not get_tenants(tenant):
        raise Exception(f"Tenant {tenant} not Present")


def check_model_name(model_name: str):
    if model_name in get_model_list():
        raise Exception(f"Model Name {model_name} already exists")


def check_group(group_name: str, parameter: dict):
    groups = get_groups()  # returns a list of dictionaries having group name as key and id as value
    group_id = ""
    if group_name not in [val.get('name') for val in groups]:
        _logger.info(f"Group {group_name} does not exist, creating a group")
        create_group(parameter)
    else:
        for val in groups:
            if val.get('name') == group_name:
                group_id = val.get('id')
        add_model_to_group(parameter.get('datamodel_name'), group_id, parameter.get('permission'))
