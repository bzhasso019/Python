from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
# from django.db import connection
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import psycopg2

@require_GET
@csrf_protect
def registration_page(request):
    connection = psycopg2.connect("dbname=test user=postgres password=19990227 host=localhost port=5432")
    password = str(request.GET.get('password'))
    login = str(request.GET.get('login'))

    if not (password or login):
        return JsonResponse({
            'status'
        })

    cursor = connection.cursor()
    cursor.execute(f"select * from users where login = '{login}'")
    connection.commit()

    result = cursor.fetchall()

    if result != []:
        cursor.close()
        connection.close()

        return JsonResponse({
            'status':'error',
            'data':'Такой логин уже существует'
        })

    else:
        cursor.execute(f"insert into users(login, password) values('{login}','{password}')")
        connection.commit()
        cursor.close()
        connection.close()

        return JsonResponse({
            'status':'success',
            'data':'Успешная регистрация'
        })



@require_GET
@csrf_protect
def authorization_page(request):
    connection = psycopg2.connect("dbname=test user=postgres password=19990227 host=localhost port=5432")
    password = request.GET.get('password')
    login = request.GET.get('login')

    cursor = connection.cursor()
    cursor.execute(f"select * from users where login='{login}' and password='{password}'")
    connection.commit()
    result = cursor.fetchall()
    cursor.close()

    if result != []:
        connection.close()
        return JsonResponse({
            'status':'success',
            'data':'Успешная авторизация'
        })

    cursor = connection.cursor()
    cursor.execute(f"select * from users where login='{login}'")
    connection.commit()
    result = cursor.fetchall()

    if result != []:
        cursor.close()
        connection.close()
        return JsonResponse({
            'status':'error',
            'data':'Неправильный пароль'
        })

    cursor.close()
    connection.close()

    return JsonResponse({
        'status':'error',
        'data':'Неправильный логин'
    })