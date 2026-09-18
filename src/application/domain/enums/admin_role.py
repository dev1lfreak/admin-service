from enum import StrEnum


class AdminRole(StrEnum):
    OPERATOR = 'operator'
    COMPLIANCE = 'compliance'
    SUPERADMIN = 'superadmin'
