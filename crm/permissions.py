from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from users.models import MANAGEMENT, SALES, SUPPORT
from crm.models import Client, Contract


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.team == MANAGEMENT and request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ClientPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.team == SUPPORT:
            return request.method in permissions.SAFE_METHODS

        return request.user.team == SALES

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.team == SALES and obj.status is False

        elif request.user.team == SUPPORT and request.method in permissions.SAFE_METHODS:
            return obj in Client.objects.filter(contract__event__support_contact=request.user)

        return request.user == obj.sales_contact or obj.status is False


class ContractPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.team == SUPPORT:
            return request.method in permissions.SAFE_METHODS

        return request.user.team == SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
    
            if request.user.team == SUPPORT:
                return obj in Contract.objects.filter(event__support_contact=request.user)

            return request.user == obj.sales_contact

        elif request.method == 'PUT' and obj.status is True:
            raise PermissionDenied("Cannot update a signed contract.")

        return request.user == obj.sales_contact and obj.status is False


class EventPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.team == SUPPORT:
            return request.method in ['GET', 'PUT']

        return request.user.team == SALES

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.support_contact or request.user == obj.contract.sales_contact

        else:
            if obj.event_status is True:
                raise PermissionDenied("Cannot update a finished event.")

            if request.user.team == SUPPORT:
                return request.user == obj.support_contact

            return request.user == obj.contract.sales_contact
