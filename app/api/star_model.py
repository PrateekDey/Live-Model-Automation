from app.api.table_handle import table_schema_data, orient_columns, add_relation
from app.api.live_models import add_table, publish_model, get_basic_model
from app.api.validations import check_group
from app.setup_structlog import get_logger
from app import arguments

_logger = get_logger(arguments.PROGRAM_NAME)


def add_query(parameter: dict):
    schema = parameter.get('schema')

    for table in parameter['table_list'].keys():
        table_id = parameter['table_list'][table]['table id']

        if parameter['table_list'][table]['Partner Type Code']:
            query = f"SELECT * FROM \"{schema}\".\"{table_id}\" where \"Partner Type Code\" ='{table.lower()}'"
        else:
            query = f"SELECT * FROM \"{schema}\".\"{table_id}\" "

        parameter['table_list'][table]['query'] = query


def automateStarModel(parameter: dict):
    _logger.info(f"Automating the process of datamodel creation for {parameter.get('table_choice')}")
    table_record = get_basic_model(parameter)

    main_table = list(table_record.get('main_table').attribute_values.keys())[0]
    secondary_tables = list(table_record.get('secondary_tables').attribute_values.keys())

    parameter['table_list'] = table_record.get('secondary_tables').attribute_values
    parameter['table_list'].update(table_record.get('main_table').attribute_values)

    add_query(parameter)

    for table_name in parameter['table_list']:

        meta_schema = table_schema_data(parameter, table_name, parameter['table_list'][table_name]['query'])

        column_list = orient_columns(meta_schema['columns'])
        response = add_table(parameter, table_name, parameter['table_list'][table_name]['table id'],
                             column_list, parameter['table_list'][table_name]['query'])
        parameter['table_list'][table_name]['table oid'] = response['oid']

        if table_name in secondary_tables:
            parameter['table_list'][table_name][parameter['table_list'][table_name]['id']] = \
                [col['oid'] for col in response['columns'] if col['id'] == parameter['table_list'][table_name]['id']][0]
        else:
            parameter['main_table_columns'] = response['columns']

    for table_name in secondary_tables:
        col_id_from_main = [col['oid'] for col in parameter['main_table_columns']
                            if col['id'] == parameter['table_list'][table_name]['id']][0]
        add_relation(parameter, main_table, col_id_from_main, table_name)

    publish_model(parameter)
    check_group(parameter.get('datagroup_name'), parameter)
