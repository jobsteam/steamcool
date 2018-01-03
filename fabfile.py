from stationery.apps.fabric_utils.fabric_class import (
    add_class_methods_as_functions,
    DjangoFabric
)


class Fabric(DjangoFabric):
    host = '89.223.26.151'
    app_name = 'key_market'
    repository = 'git@github.com:jobsteam/steamcool.git'
    remote_db_name = 'stationery'
    local_db_name = 'key_market'
    use_bower = True


__all__ = add_class_methods_as_functions(Fabric(), __name__)
