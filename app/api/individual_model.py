from app.api.live_models import add_table, publish_model, get_basic_model
from app.api.table_handle import table_schema_data, orient_columns
from app.api.validations import check_group
from app.setup_structlog import get_logger
from app import arguments

_logger = get_logger(arguments.PROGRAM_NAME)


def automateIndividualModel(parameter: dict):
    _logger.info(f"Automating the process of datamodel creation for {parameter.get('table_choice')}")
    table_record = get_basic_model(parameter)

    parameter['table'] = dict()
    parameter.get('table')['table_name'] = table_record.get('table')
    parameter.get('table')['table_id'] = table_record.get('table_id')

    parameter.get('table')['query'] = \
        f"SELECT * FROM \"{parameter.get('schema')}\".\"{table_record.get('table_id')}\" "

    meta_schema = table_schema_data(parameter, table_record.get('table_name'), parameter.get('table').get('query'))
    column_list = orient_columns(meta_schema.get('columns'))
    add_table(parameter, table_record.get('table_name'), table_record.get('table_id'), column_list,
              parameter.get('table').get('query'))

    publish_model(parameter)
    check_group(parameter.get('datagroup_name'), parameter)
