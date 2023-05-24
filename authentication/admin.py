# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Employee


# admin.site.register(Employee)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'is_superuser', 'date_joined')

    class Meta:
        ordering = ("first_name", "last_name")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        sales_group = Group.objects.get(name='sales')
        support_group = Group.objects.get(name='support')

        obj.save()

        if obj.role == 'sales':
            obj.groups.add(sales_group)
        elif obj.role == 'support':
            obj.groups.add(support_group)
