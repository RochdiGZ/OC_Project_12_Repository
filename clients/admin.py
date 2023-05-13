# Register your models here.
from django.contrib import admin
from clients.models import Client, Contract, ContractStatus

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(ContractStatus)
