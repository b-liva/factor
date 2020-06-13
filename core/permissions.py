from enum import Enum


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class OrderPermissions(BasePermissionEnum):
    ADD_REQUESTS = 'request.add_requests'
    READ_REQUESTS = 'request.read_requests'
    UPDATE_REQUESTS = 'request.update_requests'
    DELETE_REQUESTS = 'request.delete_requests'

    ADD_REQSPEC = 'request.add_reqspec'
    READ_REQSPEC = 'request.read_reqspec'
    UPDATE_REQSPEC = 'request.update_reqspec'
    DELETE_REQSPEC = 'request.delete_reqspec'


class ProformaPermissions(BasePermissionEnum):
    ADD_PROFORMA = 'request.add_xpref'
    READ_PROFORMA = 'request.read_xpref'
    UPDATE_PROFORMA = 'request.update_xpref'
    DELETE_PROFORMA = 'request.delete_xpref'

    ADD_PREF_SPEC = 'request.add_prefspec'
    READ_PREF_SPEC = 'request.read_prefspec'
    UPDATE_PREF_SPEC = 'request.update_prefspec'
    DELETE_PREF_SPEC = 'request.delete_prefspec'


class IncomePermissions(BasePermissionEnum):
    ADD_INCOME = 'incomes.add_income'
    READ_INCOME = 'incomes.read_income'
    UPDATE_INCOME = 'incomes.update_income'
    DELETE_INCOME = 'incomes.delete_income'

    ADD_INCOME_ROW = 'incomes.add_incomerow'
    READ_INCOME_ROW = 'incomes.read_incomerow'
    UPDATE_INCOME_ROW = 'incomes.update_incomerow'
    DELETE_INCOME_ROW = 'incomes.delete_incomerow'


class PaymentPermissions(BasePermissionEnum):
    ADD_PAYMENT = 'request.add_payment'
    READ_PAYMENT = 'request.read_payment'
    UPDATE_PAYMENT = 'request.update_payment'
    DELETE_PAYMENT = 'request.delete_payment'
