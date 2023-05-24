# authentication/views.py
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters

from .serializers import UserSerializer
from permissions import EmployeePermission
from .models import Employee


class EmployeeViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete an employee instance.
    """
    serializer_class = UserSerializer
    queryset = Employee.objects.all()
    permission_classes = [DjangoModelPermissions, EmployeePermission]
    search_fields = ['email', 'role']
    filter_backends = (filters.SearchFilter,)

    def list(self, request, *args, **kwargs):
        queryset = Employee.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Employee.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            employee_to_delete = Employee.objects.get(id=self.kwargs['pk'])

            if employee_to_delete == request.user:
                return Response(
                    {'message': "You can not delete yourself !"},
                    status=status.HTTP_403_FORBIDDEN)

            if employee_to_delete.id == 1:
                return Response(
                    {'message': "You can not delete the first manager !"},
                    status=status.HTTP_403_FORBIDDEN)

            self.perform_destroy(employee_to_delete)
            return Response(
                {'message': "This employee is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This employee doesn't exist")


def home(request):
    if request.user.is_authenticated:
        response = ("<h2><li>\n"
                    "   <a href=http://127.0.0.1:8000/admin/>http://127.0.0.1:8000/admin/</a>\n"
                    "</li></h2>"
                    "<h2><li>\n"
                    "   <a href=http://127.0.0.1:8000/crm/>http://127.0.0.1:8000/crm/</a>\n"
                    "</li></h2>"
                    "<h2><li>\n"
                    "   <a href=http://127.0.0.1:8000/logout/>http://127.0.0.1:8000/logout/</a>\n"
                    "</li></h2>"
                    )
        return HttpResponse(response)
    response = ("<h2><li>\n"
                "   <a href=http://127.0.0.1:8000/admin/>http://127.0.0.1:8000/admin/</a>\n"
                "</li></h2>"
                "<h2><li>\n"
                "   <a href=http://127.0.0.1:8000/login_api/>http://127.0.0.1:8000/login_api/</a>\n"
                "</li></h2>"
                )
    return HttpResponse(response)
