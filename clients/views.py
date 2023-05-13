from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters
from django.conf import settings

from .serializers import ClientSerializer, ContractSerializer, UpdateContractSerializer, ContractStatusSerializer

from authentication.models import Employee
from .models import Client, Contract, ContractStatus

User = settings.AUTH_USER_MODEL


class ClientViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a client.
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', 'email']

    def create(self, request, *args, **kwargs):
        """
            If the request user is a sales employee :
                save this client, and add him as sales_contact.
            If the request user is superuser (manager),
                the sales_contact will be chosen by himself
        """
        employee = self.request.user
        serializer = self.get_serializer(data=request.data)

        if employee.is_superuser:
            try:
                request.data['sales_contact']
            except KeyError:
                raise ValidationError("As manager you have to specify a sales_contact")

            if request.user.is_superuser:
                current_sales_contact = Employee.objects.filter(id=request.data['sales_contact']).first()

                if not current_sales_contact:
                    response = {"Sorry, this sales employee doesn't exist"}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)

                serializer.is_valid(raise_exception=True)
                new_client = serializer.save(sales_contact=current_sales_contact)
                return Response({'new_client': self.serializer_class(new_client,
                                                                     context=self.get_serializer_context()).data,
                                 'message': 'This new client is successfully added to the crm.'
                                 },
                                status=status.HTTP_201_CREATED)

        elif employee.role == 'sales':
            serializer.is_valid(raise_exception=True)
            new_client = serializer.save(sales_contact=employee)
            return Response({'new_client': self.serializer_class(new_client,
                                                                 context=self.get_serializer_context()).data,
                             'message': 'This new client is successfully added to the crm.'
                             },
                            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
            Displays a success message to the frontend.
        """
        try:
            client_to_delete = Client.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(client_to_delete)
            return Response(
                {'message': "This client is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This client doesn't exist")


class ContractViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a contract.
    """
    queryset = Contract.objects.all()
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'amount', 'client_id__email', 'client_id__company_name']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateContractSerializer
        else:
            return ContractSerializer

    def create(self, request, *args, **kwargs):
        """
            Make sure that the sales_contact's contract
            is the one in charge of the client's contract
        """
        employee = request.user
        if employee.role == 'sales':
            current_client = Client.objects.filter(
                id=request.data['client']).first()

            if not current_client:
                response = {"Sorry, this client doesn't exist"}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            in_charge_of_client = Client.objects.filter(
                id=current_client.id, sales_contact=employee).first()

            if not in_charge_of_client:
                response = {'Sorry, You are not in charge of this client'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)

            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(sales_contact=employee)
                return Response({'new_contract': serializer.data,
                                'message':
                                 'This new contract is successfully added to the crm.'},
                                status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
            if user change status of contract to True (is signed),
            update the client status (he is not a prospect anymore),
            & add this contract to table "ContractStatus"
            & create an event.
        """
        current_contract = self.get_object()
        serializer = self.get_serializer(current_contract, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if serializer.data['status'] is True:
            signed_contract = ContractStatus.objects.filter(
                contract=current_contract)

            if not signed_contract:
                ContractStatus.objects.create(contract=current_contract)

                return Response({'new_contract': serializer.data,
                                 'message':
                                 'This contract is successfully updated. Is signed and and ready to create an event'},
                                status=status.HTTP_201_CREATED)

        else:
            return Response({'new_contract': serializer.data,
                             'message':
                             'This contract is successfully updated.'},
                            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            contract_to_delete = Contract.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(contract_to_delete)
            return Response(
                {'message': "This contract is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This contract doesn't exist")


class ContractStatusViewSet(viewsets.ModelViewSet):
    """
    Read & retrieve all signed contracts.
    """
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [DjangoModelPermissions]
