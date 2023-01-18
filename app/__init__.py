import argparse

'''
    Initialises arguments

    Command Line Arguments:
    parameter
        TENANT - Tenant name
        CASE - Use case for the tenant
        ENV - Environment in which the model is to be created ['dev', 'stage', 'prod', 'demo']
        REGION - AWS region where the model is to be created ['US-EAST-1', 'EU-WEST-1', 'AP-NORTHEAST-1']
        MODEL_CHOICE - Multiple model choice entered separated by comma
        TABLE_NAME - Multiple custom names entered in the same sequence for the models selected
        MODEL_PERMISSION - Model view and edit access for the tenant

'''

argument = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
argument.add_argument(
    "--tenant", dest="tenant", required=True, help="Tenant Name"
)
argument.add_argument(
    "--case", dest="case", required=True, help="Use Case"
)
argument.add_argument(
    "--env", dest="env", required=True, help="Environment"
)
argument.add_argument(
    "--region", dest="aws_region", required=True, help="Region"
)
argument.add_argument(
    "--model-choice", dest="model_choice", required=True, help="Multiple Model Selection"
)
argument.add_argument(
    "--table-name", dest="table_name", required=True, help="Table Names Input"
)
argument.add_argument(
    "--model-permission", dest="model_permission", default="Can View Dashboard",
    help="Model Permission default to Can View Permission"
)

'''
Command Line parameters:(default set)
    PID - password id for the password portal
    API_KEY - Password Portal access key
    PASSWORD_URL - Password Portal url
    PORT_NUM - DynamoDb access port number
    Live_Model_Automation - DynamoDb table for attributes associated with each table
    datalake_table - DynamoDb table for the tenant list
    
'''

argument.add_argument(
    "--pid", dest="pid", default="1928", help="Password Id default set to 1928"
)
argument.add_argument(
    "--api-key", dest="api_key", default="d5e6b79384f3ca278eb2cd34a596f352",
    help="Password portal access key default value used"
)
argument.add_argument(
    "--password-url", dest="password_url", default="https://passwords.syncron.team", help="Password portal URL"
)
argument.add_argument(
    "--port-num", dest="port_num", default="5439", help="Default port number for the dynamoDb"
)
argument.add_argument(
    "--live-model-automation-table", dest="live_model_automation_table", default="live_model_automation",
    help="Live Model Automation table default value used"
)
argument.add_argument(
    "--datalake-tenants-table", dest="datalake_tenants_table", default="datalake-system-tenant-conf",
    help="Datalake tenants table default value used"
)
argument.add_argument(
    "--logger", dest="PROGRAM_NAME", default="Live_Model_Automation", help="Logger INFO"
)

arguments = argument.parse_args()
hostname = "https://insights." + arguments.aws_region[:2] + ".anls.syncroncloud." + \
           {'prod': 'com', 'stage': 'io', 'test': 'io', 'demo': 'io', 'dev': 'team'}.get(arguments.env.lower())
