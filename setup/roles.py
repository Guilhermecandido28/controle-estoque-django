from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'dados_financeiros': True,
    }

class Vendedor(AbstractUserRole):
        available_permissions = {
        'dados_financeiros': False,
    }