import shutil

from django.views.decorators.csrf import csrf_exempt
from .import models
import base64
import time
from django.http import JsonResponse
from lxml import etree
from django.core import signing
import os
import json
from pathlib import Path
from django.db.models import Q

# from models import User
# from models import Goods
MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent.parent, 'backend/Admin')
def ok(data: object):
    return JsonResponse({'code': 0, 'message': '操作成功', 'data': data})
def err(data: object):
    return JsonResponse({'code': 1, 'message': '操作失败', 'data': data})

#登录验证
@csrf_exempt
def login(request):
    username = request.POST.get("username")
    password = request.POST.get('password')
    print(username)
    print(password)
    user = models.UserInfo.objects.filter(user_name=username).values()
    if len(user) == 0:
        user = models.UserInfo.objects.filter(email=username).values()
        if len(user) == 0:
            date = {'flag': 'no', 'msg': 'noUser'}
            return JsonResponse({'request': date})
    userinfo = user[0]
    print(userinfo)
    if password == userinfo.get('password', 'null'):
        date_msg = "success"
        print('成功')
    else:
        date_msg = 'pwdError'
    date = {'flag': date_msg, 'msg': userinfo}
    return JsonResponse({'request': date})

# 注册时创建文件夹
def createUserFolder(username):
    filename = ['database', 'task']
    for f in filename:
        url = os.path.join(MEDIA_ROOT, 'UserAdmin', username, f).replace('\\', '/')
        if not os.path.exists(url):
            print('create')
            os.makedirs(url)
    print('create success')

#注册
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
            user = models.UserInfo(user_name=_username, email=_email, password=_password)
            user.save()
            createUserFolder(_username)
            date_msg = "success"
            date_flag = "yes"
        except:
            date_msg = 'signupError'
            date_flag = 'no'
    else:
        date_flag = 'no'
    date = {'flag': date_flag, 'msg': date_msg}
    return JsonResponse({'request': date})

def toCreateML(filename, xmin, ymin, xmax, ymax, tags, taskname):
    image_name = filename
    annotations = []
    for i in range(len(xmin)):
        label = tags[i]
        x = (int(xmin[i]) + int(xmax[i])) / 2
        y = (int(ymin[i]) + int(ymax[i])) / 2
        width = int(xmax[i]) - int(xmin[i])
        height = int(ymax[i]) - int(ymin[i])
        coordinates = dict(zip(['x', 'y', 'width', 'height'], [x, y, width, height]))
        anno = dict(zip(['label', 'coordinates'], [label, coordinates]))
        annotations.append(anno)
    createML = dict(zip(['image', 'annotations'], [image_name, annotations]))
    res = '[' + json.dumps(createML) + ']'
    url = os.path.join(MEDIA_ROOT, 'TaskAdmin', taskname, 'Annotations').replace('\\', '/')
    print(url)
    imgfile = url + '/' + filename.replace('.jpg', '.json')
    print(imgfile)
    f = open(imgfile, "w")
    f.write(res)
    print(res)
    return ok(res)

def toVoc(filename, width, height, xmin, ymin, xmax, ymax, tags, taskname):
    # 创建一个annotion节点
    root = etree.Element('annotion')
    # 创建一个子节点folder，一定要指定父节点
    child1 = etree.SubElement(root, 'folder')
    child1.text = 'VOCtype'

    child2 = etree.SubElement(root, 'filename')
    child2.text = filename

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

    url = os.path.join(MEDIA_ROOT, 'TaskAdmin', taskname, 'Annotations').replace('\\', '/')
    print(url)
    imgfile = url + '/' + filename.replace('.jpg', '.xml')
    tree = etree.ElementTree(root)
    tree.write(imgfile, pretty_print=True)


# 导出图片标签
@csrf_exempt
def label(request):
    _filename = request.POST.get("filename")
    _taskname = request.POST.get("taskname")
    _type = request.POST.get("type")
    _width = request.POST.get("width")
    _height = request.POST.get("height")
    _xmin = request.POST.getlist("xmin")
    _ymin = request.POST.getlist("ymin")
    _xmax = request.POST.getlist("xmax")
    _ymax = request.POST.getlist("ymax")
    _tags = request.POST.getlist("tags")
    print(_filename)
    print(_taskname)
    print(_type)
    print(_width)
    print(_height)
    print(_xmin)
    print(_ymin)
    print(_xmax)
    print(_ymax)
    print(_tags)
    info = 'yes'
    if(_type == 'PascalVoc'):
        toVoc(_filename, _width, _height, _xmin, _ymin, _xmax, _ymax, _tags, _taskname)
    if(_type == 'createML'):
        toCreateML(_filename, _xmin, _ymin, _xmax, _ymax, _tags, _taskname)
    return ok({})

# 上传图片
@csrf_exempt
def upload(request):
    print('get')
    print('get id')
    username = request.POST.get("username")
    print(username)
    file=request.FILES.get("file")
    print(file)
    new_img = models.LabelImg(img=file, publish_user_id=username)
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
    print('video2img')
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
        image_url = os.path.join(MEDIA_ROOT, 'UserAdmin', username, 'database', '%s.jpg' % image_name).replace(
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

# 创建任务
@csrf_exempt
def createTask(request):
    print('createTask')
    username = request.POST.get("username")
    print(username)
    # dynamicTags = request.POST.get("dynamicTags")
    taskname = request.POST.get("taskname")
    task = models.Task.objects.filter(Q(task_name=taskname) & Q(publish_user_id=username))
    if len(task) != 0:
        return err({})
    desc = request.POST.get("desc")
    print(username)
    imglist = request.POST.getlist("imglist")
    print(imglist)
    task_url = os.path.join(MEDIA_ROOT, 'TaskAdmin', taskname).replace('\\', '/')
    f = ['Img', 'Annotations']
    for i in f:
        url = os.path.join(task_url, i).replace('\\', '/')
        if not os.path.exists(url):
            os.makedirs(url)

    dest_url = os.path.join(MEDIA_ROOT, 'TaskAdmin', taskname).replace('\\', '/')
    for img in imglist:
        img_dir=os.path.join(MEDIA_ROOT, 'UserAdmin', username, 'database', img).replace('\\', '/')
        print(img_dir)
        img_object = models.LabelImg.objects.get(img=img_dir)
        task = models.Task(publish_user_id = username, task_name = taskname, description=desc, img=img_object)
        task.save()
        # 保存到task文件夹
        img_dir = str(img_dir)
        img_dest = os.path.join(dest_url, 'Img', img).replace('\\', '/')
        shutil.copy(img_dir, img_dest)

    return ok({})

# 任务列表
@csrf_exempt
def getTasklist(request):
    data = models.Task.objects.values('task_name', 'status', 'description').distinct()
    task_list = []
    index = 1
    for d in data:
        t_taskname = d['task_name']
        temp = models.Task.objects.filter(task_name=t_taskname).values()
        obj = temp[0]
        task_list.append({
            "id" : index,
            "task_name": d['task_name'],
            "status": d['status'],
            "description": d['description'],
            "publish_user_id": obj['publish_user_id'],
            "claim_user_id": obj['claim_user_id']
        })
        index += 1
    print(task_list)
    return ok(task_list)

# 标注界面的图片
@csrf_exempt
def getImglist(request):
    username = request.POST.get('username')
    # database = request.POST.get('database')
    taskname = request.POST.get('taskname')
    print(username)
    print(taskname)
    # taskname = 'newTask'
    imgs = models.Task.objects.filter(task_name=taskname).values('img_id')
    print(imgs)
    filenames = []
    b64 = []
    for i in imgs:
        img = models.LabelImg.objects.get(id=i.get('img_id'))
        url = str(img.img)
        print(url)
        filename = url[url.rfind('/') + 1 : len(url)]
        print('filename: ' + filename)
        f = open(str(img.img), 'rb')
        res = f.read()
        s = base64.b64encode(res)
        filenames.append(filename)
        b64.append(str(s)[2: len(str(s)) - 1])
    return JsonResponse({'code': 0, 'filename': filenames, 'base64': b64})

# 领取任务
@csrf_exempt
def claimTask(request):
    username = request.POST.get('username')
    taskname = request.POST.get('taskname')
    print('claim task')
    print(username)
    print(taskname)
    task = models.Task.objects.filter(task_name = taskname)
    for t in task:
        t.claim_user = models.UserInfo.objects.get(user_name = username)
        t.status = '已领取'
        t.save()
    return ok("success")

# 创建任务时显示图片
@csrf_exempt
def getTaskImg(request):
    username = request.POST.get('username')
    database = request.POST.get('database')
    print(username)
    url = os.path.join(MEDIA_ROOT, 'UserAdmin', username, 'database').replace('\\', '/')
    print(url)
    imglist = os.listdir(url)
    imgNum = len(imglist)
    print(imgNum)
    print(imglist)
    imgname = []
    imgb64 = []
    for img in imglist:
        print(img)
        f = open(url + '/' + img, 'rb')
        res = f.read()
        s = base64.b64encode(res)
        s = str(s)[2: len(str(s)) - 1]
        imgname.append(img)
        imgb64.append(s)
    return JsonResponse({'code': 0, 'filename': imgname, 'base64': imgb64})

@csrf_exempt
def getUserTask(request):
    username = request.POST.get('username')
    task = models.Task.objects.filter(claim_user_id=username).values('task_name').distinct()
    tasklist = []
    for i in task:
        t = i['task_name']
        tasklist.append(t)
    print(username)
    print(tasklist)
    return ok(tasklist)
