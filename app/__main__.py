from app import arguments
from api import star_model, individual_model
from api.connect_password import password_details
from api.validations import check_if_tenant_exists, check_model_name


def main():
    dg_tenant = tenant = arguments.tenant.lower()
    dg_case = case = arguments.case.lower()
    env = arguments.env.lower()

    model_choice_list = list(map(str.strip, arguments.model_choice.split(",")))
    table_name_list = list(map(str.strip, arguments.table_name.split(",")))

    model_permission = {
        "Can View Dashboard": 'a',
        "Can Edit Model": 'w',
        "Can View and Create Dashboard": 'r'
    }.get(arguments.model_permission)

    for model_choice, table_name in zip(model_choice_list, table_name_list):
        if model_choice == "Registration Fact":
            tenant, case = "product", "sf"

        check_if_tenant_exists(f'{tenant}_{case}_{env}')
        check_model_name(f"{tenant}_{case}_{env}_{table_name}")

        password_param = password_details(tenant, case, env)

        parameter = {
            "datamodel_name": f"{dg_tenant}_{dg_case}_{env}_{table_name}",
            "dataset_name": f"{dg_tenant}_{dg_case}_{env}_{table_name}_set",
            "datagroup_name": f"{dg_tenant}_{dg_case}_{env}",
            "schema": f"{tenant}_{case}_{env}",
            "table_choice": model_choice,
            "permission": model_permission,
            "provider": "RedShift"
        }

        parameter.update(password_param)

        if model_choice == "Registration Fact":
            star_model.automateStarModel(parameter)
        else:
            individual_model.automateIndividualModel(parameter)


main()
