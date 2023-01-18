import boto3
from app.setup_structlog import get_logger
from app import arguments

_logger = get_logger(arguments.PROGRAM_NAME)


def get_ssm_client():
    return boto3.client('ssm', region_name=arguments.aws_region)


class ParameterNotFoundException(Exception):
    def __init__(self, name):
        self.name = name


def get_ssm_parameter(parameter_name):
    try:
        ssm_param = get_ssm_client().get_parameter(Name=parameter_name, WithDecryption=True)
        return ssm_param['Parameter']['Value']
    except Exception:
        _logger.critical('SSM parameter not found', parameter_name=parameter_name)
        raise ParameterNotFoundException(parameter_name)
