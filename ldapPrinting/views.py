from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import base64
import requests
import json
from django.conf import settings
import os
from django.forms.models import model_to_dict


@csrf_exempt
def validate_token(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            token = body['token']
            token_obj = session.objects.get(key=token)
            user = token_obj.user
            return JsonResponse({'status': 'success', "success": True, "user": user.username})
        except:
            return JsonResponse({'status': 'failure', "success": False})


@csrf_exempt
def profile(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            token = body['token']
            token_obj = session.objects.get(key=token)
            user = token_obj.user
            user = model_to_dict(user)
            return JsonResponse({'status': 'success', "success": True, "user": json.dumps(user)})
        except Exception as e:
            return JsonResponse({'status': 'failure', "success": False, "error": str(e)})


@csrf_exempt
def authentication(request):

    print("authentication called")

    headers = {"Authorization": "Basic "
               + base64.b64encode(
                   f"bsvKH9AqOUkDJIesV34cYlsseocAZGhc9kW88Lz1:582T6oWVYPQwrBiL8C8mT65BPlPslJFryf8eLDXrZ6ThcoqwXsfbRcNhCrE7t37ANJzzU6spdaEBMApheXADDcxvPUaBdNPdtgag6no0POVU7PA5PGbCifb9WFfI1Shw".encode(
                       "utf-8")
               ).decode("utf-8"),
               "Content-Type": "application/x-www-form-urlencoded",
               }
    x = base64.b64encode(
        f"bsvKH9AqOUkDJIesV34cYlsseocAZGhc9kW88Lz1:582T6oWVYPQwrBiL8C8mT65BPlPslJFryf8eLDXrZ6ThcoqwXsfbRcNhCrE7t37ANJzzU6spdaEBMApheXADDcxvPUaBdNPdtgag6no0POVU7PA5PGbCifb9WFfI1Shw".encode(
            "utf-8")
    ).decode("utf-8")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['code']
    print(content)
    r = requests.post('https://gymkhana.iitb.ac.in/profiles/oauth/token/',
                      data='code='+content+'&grant_type=authorization_code', headers=headers)
    print(r.json())
    b = requests.get('https://gymkhana.iitb.ac.in/profiles/user/api/user/?fields=first_name,last_name,type,username,profile_picture,email,mobile,roll_number,program,insti_address',
                     headers={'Authorization': 'Bearer '+r.json()['access_token']})
    data = b.json()
    try:
        user = User.objects.get(username=data['username'])
        if user:
            token, created = session.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
    except Exception as e:
        print(e)

    user = User(first_name=data['first_name'], last_name=data['last_name'], username=data['username'], email=data['email'], roll_number=data['roll_number'], department_name=data['program']
                ['department_name'], degree_name=data['program']['degree_name'], graduation_year=data['program']['graduation_year'], join_year=data['program']['join_year'], hostel_name=data['insti_address']['hostel_name'], hostel=data['insti_address']['hostel'], room=data['insti_address']['room'])
    user.save()
    token = session.objects.create(user=user, key=r.json()['access_token'])
    token.save()
    return JsonResponse({'token': token.key})
