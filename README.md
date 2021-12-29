# BS project ImageAnnotation Web
> 2021 秋冬 《B/S体系软件设计课程大作业》 数据集标注网站

## 文件目录
```shell
├─Admin
│  └─TaskAdmin
│  └─UserAdmin
├─backend
│  └─backend
│  └─Admin
│  └─ImageAnnotation
│  └─manage.py
├─frontend
│  └─dist
│  └─node_modules
│  └─public
│  └─src  
│  └─test     
```
- Admin: 存储任务、用户信息

- backend: 后端文件夹 
  
  python django + MySQL
  
- frontend: 前端文件夹

  vue + element ui


## 配置运行
- 配置虚拟环境
    ```shell
    cd backend   #到backend目录下
    mkvirtualenv <django> #创建虚拟环境<虚拟环境名>
    pip install -r requirements.txt #安装相关包
    workon django #在虚拟环境下运行
    ```

- 迁移数据库

  在/backend/ImageAnnotation/settings.py中有相关的数据库设置，需要在本地的MySQL中创建相应的数据库，并修改USER, PASSWORD, HOST, PORT来连接相应的数据库。
  ```python
  DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # 数据库的类型
            'NAME': 'image_annotation', #所使用的数据库的名字
            'USER': 'root', #数据库服务器的用户
            'PASSWORD': '123456', #密码
            'HOST': '127.0.0.1', #主机
            'PORT': '3306', #端口
        }
    }
  ```
  数据库连接完成后，进行数据库迁移
    ```shell
    python manage.py makemigrations
    python mange.py migrate
    ```

- 运行
  
  前后端已经部署整合完成，直接运行后端`manage.py`文件即可，运行完成后按提示访问 http://127.0.0.1:8000/
    ```shell
    python manage.py runserver #
    ```

