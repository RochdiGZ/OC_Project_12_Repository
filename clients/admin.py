# Register your models here.
from django.contrib import admin
from customers.models import Customer, Contract

admin.site.register(Customer)


class ContractAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['company_name', 'get_company_name', ]

    def get_company_name(self, obj):
        return obj.author.company_name
    get_company_name.admin_order_field = 'customer'  # Allows column order sorting
    get_company_name.short_description = 'Company Name'  # Renames column head

    # Filtering on side - for some reason, this works
    # list_filter = ['company_name', 'customer__company_name']


admin.site.register(Contract, ContractAdmin)
