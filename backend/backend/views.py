from django.views.decorators.csrf import csrf_exempt
from .import models
from django.http import JsonResponse
import os
from ImageAnnotation import settings as setting
# from models import User
# from models import Goods


@csrf_exempt
def login(request):
    username = request.POST.get("username")
    password = request.POST.get('password')
    print(username)
    print(password)
    try:
        user = models.User.objects.get(user_name=username)
        print(user)
    except:
        date = {'flag': 'no', 'msg': 'noUser'}
        print("noUser")
        return JsonResponse({'request':date})

    if password == user.password:
        date_msg = "success"
        date_flag = "yes"
        print('成功')
    else:
        date_msg = 'pwdError'
        date_flag = 'no'
    date = {'flag': date_flag, 'msg': date_msg}

    return JsonResponse({'request':date})

@csrf_exempt
def signup(request):
    _username = request.POST.get("username")
    _email = request.POST.get("email")
    _password = request.POST.get("password")
    print(_username)
    print(_email)
    print(_password)
    date_msg = ''
    response_username = models.User.objects.filter(user_name=_username)
    if(len(response_username) > 0):
        date_msg = "usernameInvalid"
        date_flag = "no"
        date = {'flag': date_flag, 'msg': date_msg}
        return JsonResponse({'request': date})
    response_email = models.User.objects.filter(email=_email)

    if(len(response_email) > 0):
        date_msg = "emailInvalid"
        date_flag = "no"
        date = {'flag': date_flag, 'msg': date_msg}
        return JsonResponse({'request': date})

    if(date_msg == ''):
        try:
            user = models.User(user_name=_username, email=_email, password=_password)
            user.save()
            date_msg = "success"
            date_flag = "yes"
        except:
            date_msg = 'signupError'
            date_flag = 'no'
    else:
        date_flag = 'no'
    date = {'flag': date_flag, 'msg': date_msg}
    return JsonResponse({'request': date})

@csrf_exempt
def post(request):
    res={}
    name = request.data.get('name')
    price = request.data.get('price')
    image = request.data.get('file')
    print(name)
    print(price)
    print(image)
    if not all([name,price,image]):
        res['code']=10020
        res['message']='输入不能为空'
    else:
        image_name = image.name
        image_path = os.path.join(setting.UPLOAD_FILE,image_name)
        f = open(image_path,'wb')
        for i in image.chunks():
            f.write(i)
        f.close()
        goods = models.Goods.objects.filter(name=name).first()
        if goods:
            res['code']=10023
            res['message']='商品已存在'
        else:
            goods = models.Goods(name=name,price=price,image='/upload/'+image_name)
            goods.save()
            res['code']=200
            res['message']='添加成功'
            return JsonResponse(res)
    return JsonResponse(res)