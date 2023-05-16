# Register your models here.
from django.contrib import admin
from authentication.models import Employee

# admin.site.register(Employee)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'is_superuser', 'date_joined')

    class Meta:
        ordering = ("first_name", "last_name")
