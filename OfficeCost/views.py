from django.shortcuts import render
from datetime import datetime
from django.views.decorators.http import require_http_methods
import cx_Oracle
from django.db import connection
from OfficeCost.models import *
import re
from django.http import Http404


# @require_http_methods(['GET', 'POST'])
# from time import time

def index(request):
    return render(request, 'officecost/index.html', {})


@require_http_methods(['GET', 'POST'])
def add(request):
    error = False
    success = False
    if request.user.is_authenticated() and request.method == 'POST' \
            and request.user.employe_id != None:
        success = True
        try:
            amount = float(request.POST['amount'])
            dic = get_expense_types(request.user)
            expensetypeid_in_db = dic[str(request.POST['expenseIdSelect'])][1]
            date = str(request.POST['datetime'])
            cursor = connection.cursor()
            cursor.callproc('ADD_EXPENSE', [expensetypeid_in_db, amount, date, request.user.employe_id_id])
        # except AttributeError:
        except Exception:
            success = False
            error = True
    now = datetime.now()
    dic = get_expense_types(request.user)
    expense_types_select = [{'val': x, 'text': dic[x][0]} for x in dic]
    return render(request, 'officecost/add.html',
                  {'date': now.strftime('%Y-%m-%d'), 'select': expense_types_select,
                   'success': success, 'error': error})


def get_expense_types(user):
    departmentsid_id = user.employe_id.departmentsid_id
    expense_types = list(Departmentsexpensetypes.objects.filter(departmentsid=departmentsid_id))
    clean_expense_types = {}
    for x, i in zip(expense_types, range(len(expense_types))):
        clean_expense_types[str(i)] = (x.expensetypesid.name, x.expensetypesid_id)
    return clean_expense_types


def get_departments():
    departments = list(Departments.objects.all())
    clean_departments = {}
    for x, i in zip(departments, range(len(departments))):
        clean_departments[str(i)] = (x.name, x.departmentid)
    return clean_departments




def my_expenses(request):
    if request.user.is_authenticated() and request.user.employe_id != None:
        startDate, finishDate = request.GET.get('startDate'), request.GET.get('finishDate')
        if startDate and finishDate:
            pattern = re.compile("\d{4}-\d\d-\d\d")
            if pattern.match(startDate) and pattern.match(finishDate):
                table = getExpensesFromDate(startDate, finishDate, None, request.user.employe_id_id)
                table = [x[:-1] for x in table]
                startDate, finishDate = convert_str_date_us_ru(startDate), convert_str_date_us_ru(finishDate)
                return render(request, 'officecost/expenses_table.html',
                              {'startDate': startDate,
                               'finishDate': finishDate,
                               'table': table,
                               'flagEmployeColomn': False})
            else:
                raise Http404('Введите верные даты!')
        else:
            finishDate = datetime.now()
            startDate = datetime(finishDate.year, finishDate.month, 1)
            return render(request, 'officecost/expenses_search.html',
                          {'finishDate': finishDate.strftime('%Y-%m-%d'),
                           'startDate': startDate.strftime('%Y-%m-%d'),
                           'department': False})
    else:
        return render(request, 'officecost/authentication error.html', {})


def department_expenses(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        startDate, finishDate = request.GET.get('startDate'), request.GET.get('finishDate')
        departmentSelect = request.GET.get('departmentSelect')
        if startDate and finishDate and departmentSelect:
            pattern = re.compile("\d{4}-\d\d-\d\d")
            if pattern.match(startDate) and pattern.match(finishDate):
                dic = get_departments()
                departmentSelect_in_db = dic[str(departmentSelect)][1]
                table = getExpensesFromDate(startDate, finishDate, departmentSelect_in_db, None)
                startDate, finishDate = convert_str_date_us_ru(startDate), convert_str_date_us_ru(finishDate)
                return render(request, 'officecost/expenses_table.html',
                              {'startDate': startDate,
                               'finishDate': finishDate,
                               'table': table,
                               'flagEmployeColomn': True})
            else:
                raise Http404('Введите верные даты!')
        else:
            finishDate = datetime.now()
            startDate = datetime(finishDate.year, finishDate.month, 1)
            dic = get_departments()
            departments_select = [{'val': x, 'text': dic[x][0]} for x in dic]
            return render(request, 'officecost/expenses_search.html',
                          {'finishDate': finishDate.strftime('%Y-%m-%d'),
                           'startDate': startDate.strftime('%Y-%m-%d'),
                           'department': True,
                           'departmentSelect': departments_select})
    else:
        return render(request, 'officecost/authentication error.html', {})


def limits(request):
    if request.user.is_authenticated() and request.user.employe_id != None:
        cursor = connection.cursor()
        department = request.user.employe_id.departmentsid_id
        department_name = request.user.employe_id.departmentsid.name
        client_cursor = cursor.callfunc('Limits', cx_Oracle.CURSOR, [0])
        data = client_cursor.fetchall()
        table = []
        for x in data:
            name = Departmentsexpensetypes.objects.get(departmentsexpensetypesid=x[0]).expensetypesid.name
            table.append((name, x[1], x[2]))
        return render(request, 'officecost/limits.html', {'table': table, 'department_name': department_name})
    else:
        return render(request, 'officecost/authentication error.html', {})


def getExpensesFromDate(startDate, finishDate, departmentid, employeid):
    data = None
    if employeid is not None:
        cursor = connection.cursor()
        client_cursor = cursor.callfunc('EMPLOYEES_EXPENSE', cx_Oracle.CURSOR, [startDate, finishDate, employeid])
        data = client_cursor.fetchall()
    else:
        cursor = connection.cursor()
        client_cursor = cursor.callfunc('DEPARTMENTED_EXPENSE', cx_Oracle.CURSOR, [startDate, finishDate, departmentid])
        data = client_cursor.fetchall()
    data.sort(key=lambda x: x[3])
    clean_data = []
    for x, i in zip(data, range(len(data))):
        time = x[3].strftime('%d.%m.%Y')
        #name = list(Employees.objects.get(employeid = x[4]))[0].name
        clean_data.append([i, x[1], x[2], time, x[4]])
    return clean_data


# def balance(request):
#     return render(request, 'officecost/balance.html', {})

def convert_str_date_us_ru(string):
    return datetime.strptime(string, '%Y-%m-%d').strftime('%d.%m.%Y')
