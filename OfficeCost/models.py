from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# class Accounts(models.Model):
#     accountid = models.BigIntegerField(primary_key=True)
#     employeid = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employeid', blank=True, null=True)
#     roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='roleid', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'accounts'



class Departments(models.Model):
    departmentid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    employeesnumber = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'departments'

class Departmentsexpensetypes(models.Model):
    departmentsexpensetypesid = models.BigIntegerField(primary_key=True)
    departmentsid = models.ForeignKey(Departments, models.DO_NOTHING, db_column='departmentsid', blank=True, null=True)
    expensetypesid = models.ForeignKey('Expensetypes', models.DO_NOTHING, db_column='expensetypesid', blank=True, null=True)
    monthlimit = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'departmentsexpensetypes'


class Employees(models.Model):
    employeid = models.BigIntegerField(primary_key=True)
    departmentsid = models.ForeignKey(Departments, models.DO_NOTHING, db_column='departmentsid')
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'employees'


class Expenses(models.Model):
    expensesid = models.BigIntegerField(primary_key=True)
    expensetypesid = models.ForeignKey('Expensetypes', models.DO_NOTHING, db_column='expensetypesid')
    amount = models.BigIntegerField()
    datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'expenses'


class Expensesemployees(models.Model):
    expensesemployeesid = models.BigIntegerField(primary_key=True)
    employeid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='employeid', blank=True, null=True)
    expensesid = models.ForeignKey(Expenses, models.DO_NOTHING, db_column='expensesid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expensesemployees'


class Expensetypes(models.Model):
    expensetypesid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    descrition = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expensetypes'


class OfficecostAccountcustom(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=256, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=508, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    name2 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'officecost_accountcustom'



class Roles(models.Model):
    roleid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'roles'


class AccountCustom(AbstractUser):
    employe_id = models.ForeignKey('Employees', models.DO_NOTHING, db_column='employeid', null=True)
    role_id = models.ForeignKey('Roles', models.DO_NOTHING, db_column='roleid', null=True)

