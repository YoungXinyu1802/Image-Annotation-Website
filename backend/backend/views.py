from django.views.decorators.csrf import csrf_exempt
from .import models
import base64
import time
from django.http import JsonResponse
from lxml import etree
from django.core import signing
import os
from pathlib import Path
# from models import User
# from models import Goods
MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent.parent, 'backend/upload_file/uploads/')
def ok(data: object):
    return JsonResponse({'code': 0, 'message': '操作成功', 'data': data})

@csrf_exempt
def login(request):
    username = request.POST.get("username")
    password = request.POST.get('password')
    print(username)
    print(password)
    try:
        user = models.UserInfo.objects.get(user_name=username)
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
    response_username = models.UserInfo.objects.filter(user_name=_username)
    if(len(response_username) > 0):
        date_msg = "usernameInvalid"
        date_flag = "no"
        date = {'flag': date_flag, 'msg': date_msg}
        return JsonResponse({'request': date})
    response_email = models.UserInfo.objects.filter(email=_email)

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

@csrf_exempt
def upload(request):
    print('get')
    # token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    # print(token)
    print('get id')
    username = request.POST.get("username")
    database = request.POST.get("database")
    print(username)
    # user_id = token['id']
    file=request.FILES.getlist("file")
    print(file)

    for f in file:
        img_url = os.path.join(MEDIA_ROOT, username, 'database', database).replace('\\', '/')
        print(img_url)
        print(os.path.exists(img_url))
        if not os.path.exists(img_url):
            print('create')
            os.makedirs(img_url)
        # new_img = models.LabelImg(img=file, publish_user_id=username)
        # new_img.save()
        _img_url = img_url + '/' + str(f)
        with open(_img_url, 'wb') as dest:
            for chunk in f.chunks():
                dest.write(chunk)
                print('load')
        new_img = models.LabelImg(img=_img_url)
        new_img.save()

    # img_list = []
    # for img in models.LabelImg.objects.filter(publish_user_id=username):
    #     img_list.append({
    #         "id": img.id,
    #         "text": img.img.name,
    #         "status": img.status,
    #         "description": img.description
    #     }
    #     )
    return ok(username)


@csrf_exempt
def video2img(request):
    imgsrc = request.POST.getlist("imgSrc")
    print(len(imgsrc))
    username = request.POST.get("username")
    print(username)

    index = 0
    for img in imgsrc:
        # print(img)
        image = img.split(",")
        result = image[1]
        image_data = base64.b64decode(result)
        image_name = str(int(time.strftime("%Y%m%d%H%M%S"))) + '_' + str(index)
        image_url = os.path.join(MEDIA_ROOT, '%s.jpg' % image_name).replace(
            '\\', '/')
        print(image_url)
        myfile = Path(image_url)
        myfile.touch(exist_ok=True)
        with open(image_url, 'wb') as f:
            f.write(image_data)  # 打开路径将结果写入到文件中
        new_img = models.LabelImg(img=image_url, publish_user_id=username)
        new_img.save()
        index += 1
    return ok(imgsrc)


@csrf_exempt
def createTask(request):
    username = request.POST.get("username")
    # dynamicTags = request.POST.get("dynamicTags")
    taskname = request.POST.get("taskname")
    desc = request.POST.get("desc")
    # resource = request.POST.get("resource")
    # imgs = request.POST.get("imgs")
    print(username)
    # print(type)
    # print(dynamicTags)
    # print(resource)
    # print(imgs)

    task = models.Task(publish_user_id = username, task_name = taskname, description=desc)
    task.save()

    return ok(username)

@csrf_exempt
def getTasklist(request):
    username = request.POST.get('username')
    print(username)
    data = models.Task.objects.all().values()
    # print(data)
    # data = models.Task.objects.filter(publish_user_id=username).values()
    # print(data[0])
    contents = list(data)
    print(contents)
    print(ok(contents))
    return ok(contents)

@csrf_exempt
def getImglist(request):

    username = request.POST.get('username')
    database = request.POST.get('database')
    url = os.path.join(MEDIA_ROOT, 'yxy1802', 'database', 'bee').replace('\\', '/')
    print(url)
    imglist = os.listdir(url)
    imgNum = len(imglist)
    print(imgNum)
    print(imglist)
    b64 = []
    for img in imglist:
        print(img)
        f = open(url + '/' + img, 'rb')
        res = f.read()
        s = base64.b64encode(res)
        b64.append(str(s)[2 : len(str(s)) - 1])
    print(ok(b64))
    return ok(b64)