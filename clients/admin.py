# Register your models here.
from django.contrib import admin
from clients.models import Client, Contract, ContractStatus, Event

# admin.site.register(Client)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                    'company_name', 'is_prospect', 'sales_contact',)

    class Meta:
        ordering = ("first_name", "last_name")


# admin.site.register(Contract)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'payment_due', 'status', 'date_created', 'date_updated',
                    'client', 'sales_contact')

    class Meta:
        ordering = ("-amount", )


# admin.site.register(ContractStatus)


@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
    list_display = ('contract', )


# admin.site.register(Event)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'attendees', 'event_date', 'notes', 'support_contact',
                    'date_created', 'date_updated', 'event_status', 'client', )

    class Meta:
        ordering = ("-date_updated", )
