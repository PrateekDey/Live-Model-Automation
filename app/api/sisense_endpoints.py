import json
from typing_extensions import TypedDict
from app import hostname

from app.aws.clients import get_ssm_parameter


API_ENDPOINT = "{}/api".format(hostname)
Headers = TypedDict('Headers', {'authorization': str})


def get_endpoint(key, *args):
    endpoint, role = endpoints.get(key)
    endpoint = endpoint.format(API_ENDPOINT, *args)
    headers = get_auth_token(role.lower())
    return endpoint, headers


def get_auth_token(role: str) -> dict:
    ssm_role_token = "insights_{}_token".format(role)
    ssm_param = get_ssm_parameter(ssm_role_token)
    auth_token = json.loads(ssm_param).get('token')
    return {'authorization': 'Bearer ' + auth_token}


endpoints: dict = {
    "create_live_cube": ["{}/v2/datamodels", 'ADMIN'],
    "create_live_dataset": ["{}/v2/datamodels/{}/schema/datasets", 'ADMIN'],
    "create_live_table": ["{}/v2/datamodels/{}/schema/datasets/{}/tables", 'ADMIN'],
    "create_relation": ["{}/v2/datamodels/{}/schema/relations", 'ADMIN'],
    "table_schema_details": ["{}/v1/connection/{}/table_schema_details", 'ADMIN'],
    "connections": ["{}/v1/connection", 'ADMIN'],
    "ecm": ["{}/v2/ecm", 'ADMIN'],
    "model_list": ["{}/v2/datamodels/schema?fields=title%2C%20type", 'ADMIN'],
    "groups_list": ["{}/v1/groups", 'ADMIN'],
    "create_group": ["{}/v1/groups?fields=name", 'ADMIN'],
    "add_model_to_group": ["{}/v1/elasticubes/cubeShares", 'ADMIN']
}
