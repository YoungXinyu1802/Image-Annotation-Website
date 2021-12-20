from django.views.decorators.csrf import csrf_exempt
from .import models
from django.http import JsonResponse
from lxml import etree
import os
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

def toVoc(filename, width, height, xmin, ymin, xmax, ymax, tags):
    # 创建一个annotion节点
    root = etree.Element('annotion')
    # 创建一个子节点folder，一定要指定父节点
    child1 = etree.SubElement(root, 'folder')
    child1.text = 'VOCtype'

    child2 = etree.SubElement(root, 'filename')
    child2.text = '000001.jpg'

    child3 = etree.SubElement(root, 'source')

    child31 = etree.SubElement(child3, 'database')
    child31.text = 'VOC'

    child4 = etree.SubElement(root, 'size')

    child41 = etree.SubElement(child4, 'width')
    child41.text = width

    child42 = etree.SubElement(child4, 'height')
    child42.text = height

    child5 = etree.SubElement(root, 'segmented')
    child5.text = '0'
    # 自定义数据集
    objectlist = []
    for i in range(0, len(xmin)):
        dic = dict(tag=tags[i], xmin=xmin[i], ymin=ymin[i], xmax=xmax[i], ymax=ymax[i])
        objectlist.append(dic)
    print(objectlist)

    for i in objectlist:
        child6 = etree.SubElement(root, 'object')

        child61 = etree.SubElement(child6, 'name')
        child61.text = str(i['tag'])

        child62 = etree.SubElement(child6, 'pose')
        child62.text = 'Unspecified'

        child63 = etree.SubElement(child6, 'truncated')
        child63.text = '0'

        child64 = etree.SubElement(child6, 'difficult')
        child64.text = '0'

        child65 = etree.SubElement(child6, 'bndbox')

        child651 = etree.SubElement(child65, 'xmin')
        child651.text = str(i['xmin'])

        child652 = etree.SubElement(child65, 'ymin')
        child652.text = str(i['ymin'])

        child653 = etree.SubElement(child65, 'xmax')
        child653.text = str(i['xmax'])

        child654 = etree.SubElement(child65, 'ymax')
        child654.text = str(i['ymax'])

    tree = etree.ElementTree(root)
    tree.write('pascal.xml', pretty_print=True)



@csrf_exempt
def label(request):
    _filename = request.POST.get("filename")
    _width = request.POST.get("width")
    _height = request.POST.get("height")
    _xmin = request.POST.getlist("xmin")
    _ymin = request.POST.getlist("ymin")
    _xmax = request.POST.getlist("xmax")
    _ymax = request.POST.getlist("ymax")
    _tags = request.POST.getlist("tags")
    print(_filename)
    print(_width)
    print(_height)
    print(_xmin)
    print(_ymin)
    print(_xmax)
    print(_ymax)
    print(_tags)
    info = 'yes'
    toVoc(_filename, _width, _height, _xmin, _ymin, _xmax, _ymax, _tags)


    return JsonResponse({'request': info})