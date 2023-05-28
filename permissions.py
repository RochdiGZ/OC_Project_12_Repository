from django.contrib.auth.models import Group, Permission
from rest_framework import permissions

from clients.models import Contract


def create_groups():
    """
        When a superuser is created
        this function is called
        to create groups permissions (sales & support)
    """

    add_client = Permission.objects.get(codename='add_client')
    change_client = Permission.objects.get(codename='change_client')
    view_client = Permission.objects.get(codename='view_client')

    add_contract = Permission.objects.get(codename='add_contract')
    change_contract = Permission.objects.get(codename='change_contract')
    view_contract = Permission.objects.get(codename='view_contract')

    add_contract_status = Permission.objects.get(codename='add_contract_status')
    change_contract_status = Permission.objects.get(codename='change_contract_status')
    view_contract_status = Permission.objects.get(codename='view_contract_status')

    add_event = Permission.objects.get(codename='add_event')
    change_event = Permission.objects.get(codename='change_event')
    view_event = Permission.objects.get(codename='view_event')

    sales_permissions = [
        add_client, change_client, view_client,
        add_contract, change_contract, view_contract,
        add_contract_status, change_contract_status, view_contract_status,
        add_event, view_event
    ]

    sales_group = Group(name='sales')
    sales_group.save()
    sales_group.permissions.set(sales_permissions)

    support_permissions = [
        view_client, view_contract,
        change_event, view_event
    ]

    support_group = Group(name='support')
    support_group.save()
    support_group.permissions.set(support_permissions)


def add_to_group(new_employee):
    """
        When an employee is created,
        this function is called
        for adding him to the corresponding group.
    """

    sales_group = Group.objects.get(name='sales')
    support_group = Group.objects.get(name='support')
    manager_group = Group.objects.get(name='manager')

    if new_employee.role == 'sales':
        new_employee.groups.add(sales_group)
    elif new_employee.role == 'support':
        new_employee.groups.add(support_group)
    else:
        new_employee.groups.add(manager_group)


NOT_ALLOWED = "You are not a manager !"
NOT_IN_CHARGE = "You are not in charge of this !"
NOT_SALES_IN_CHARGE = "You can't create this event, because you're not in charge of this contract !"


class EmployeePermission(permissions.BasePermission):
    """
        Check if the connected user is manager.
    """
    message = ""

    def has_permission(self, request, view):
        self.message = NOT_ALLOWED
        if request.user.is_superuser:
            return True
        return False


class ObjectPermission(permissions.BasePermission):
    """
        Check if the connected user
        is the main contact in charge of this contract or client;
    """
    message = ""

    def has_object_permission(self, request, view, obj):
        self.message = NOT_IN_CHARGE

        if view.action in ['list', 'retrieve', 'update'] and request.user == obj.sales_contact:
            return True

        elif request.user.is_superuser:
            return True

        else:
            return False


class EventPermission(permissions.BasePermission):
    """
        Check if the connected user
        is the main contact in charge of this event;
    """
    message = ""

    def has_permission(self, request, view):
        self.message = NOT_SALES_IN_CHARGE

        current_contract = view.kwargs.get('contract_id')
        sales_of_current_project = Contract.objects.filter(
                id=current_contract,
                sales_contact=request.user).exists()

        if sales_of_current_project:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        self.message = NOT_IN_CHARGE

        if view.action in ['retrieve', 'update'] and (request.user == obj.support_contact):
            return True
        else:
            return False
