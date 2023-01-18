from app.setup_structlog import get_logger
from app import arguments
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute
from pynamodb.exceptions import PynamoDBException

_logger = get_logger(arguments.PROGRAM_NAME)


class LiveModelAutomation(Model):
    class Meta:
        table_name = arguments.live_model_automation_table
        region = arguments.aws_region

    table = UnicodeAttribute(hash_key=True)
    main_table = MapAttribute(null=True)
    secondary_tables = MapAttribute(null=True)
    table_id = UnicodeAttribute(null=True)
    table_name = UnicodeAttribute(null=True)


class DatalakeTenants(Model):
    class Meta:
        table_name = arguments.datalake_tenants_table
        region = arguments.aws_region

    tenant_id = UnicodeAttribute(hash_key=True)
    dms = MapAttribute()
    emr = MapAttribute()
    glue_database = UnicodeAttribute()
    glue_etl = MapAttribute()
    incremental_load_spec = MapAttribute(null=True)
    s3_bucket_name = UnicodeAttribute()
    spark_runtime = UnicodeAttribute()
    timezone = UnicodeAttribute()


def get_live_model_tables(table: str):
    table_record = LiveModelAutomation.get(hash_key=table)
    return table_record.attribute_values


def get_datalake_tenants(tenant_id: str):
    try:
        if DatalakeTenants.get(hash_key=tenant_id).exists():
            return True

    except PynamoDBException:
        _logger.error(f"Tenant {tenant_id} not Present")

