from django.contrib import admin
from .models import *

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('employeid', 'departmentsid', 'name')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_superuser', 'employe_id', 'role_id')
    list_filter = ['is_superuser']


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('departmentid', 'name', 'employeesnumber')


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('expensesid', 'amount', 'datetime','expensetypesid')
    list_filter = ['datetime']

admin.site.register(AccountCustom, UserAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Expensetypes)
admin.site.register(Departmentsexpensetypes)
admin.site.register(Roles)
admin.site.register(Expensesemployees)


# Register your models here.
