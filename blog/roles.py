"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: The purpose of this code is to create
roles that may work in the system
"""
from rolepermissions.roles import AbstractUserRole


class Member(AbstractUserRole):
    """
    Outlines member permissions
    """

    available_permissions = {
        "find_minister": True,
    }


class Minister(AbstractUserRole):
    """
    Outlines minister permissions
    """

    available_permissions = {"refer_minister": True}


class Ministry(AbstractUserRole):
    """
    Outlines ministry permissions
    """

    available_permissions = {"find_minister": True}
