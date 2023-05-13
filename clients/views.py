from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import filters
from django.conf import settings

from .serializers import CustomerSerializer

from authentication.models import Employee
from .models import Customer

User = settings.AUTH_USER_MODEL


class CustomerViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a customer.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
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
                new_customer = serializer.save(sales_contact=current_sales_contact)
                return Response({'new_customer': self.serializer_class(new_customer,
                                                                       context=self.get_serializer_context()).data,
                                 'message': 'This new customer is successfully added to the crm.'
                                 },
                                status=status.HTTP_201_CREATED)

        elif employee.role == 'sales':
            serializer.is_valid(raise_exception=True)
            new_customer = serializer.save(sales_contact=employee)
            return Response({'new_customer': self.serializer_class(new_customer,
                                                                   context=self.get_serializer_context()).data,
                             'message': 'This new customer is successfully added to the crm.'
                             },
                            status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
            Displays a success message to the frontend.
        """
        try:
            customer_to_delete = Customer.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(customer_to_delete)
            return Response(
                {'message': "This customer is successfully deleted"},
                status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This customer doesn't exist")
