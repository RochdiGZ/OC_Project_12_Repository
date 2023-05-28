# Register your models here.
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django import forms
from .models import Employee


# admin.site.register(Employee)
class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith('@epicevents.com'):
            raise forms.ValidationError(
                "Please, email has to end with epicevents.com")
        return self.cleaned_data["email"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    add_form = EmployeeAdminForm
    empty_value_display = 'None'
    search_fields = ('email', )
    list_display = ['email', 'role', ]
    list_filter = ['role', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)

        sales_group = Group.objects.get(name='sales')
        support_group = Group.objects.get(name='support')
        manager_group = Group.objects.get(name='manager')

        obj.save()

        if obj.role == 'sales':
            obj.groups.add(sales_group)
        elif obj.role == 'support':
            obj.groups.add(support_group)
        else:
            obj.groups.add(manager_group)
