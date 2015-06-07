基本流程
---------
### 1:django-admin startproject mysite (version 1.8.2)
### 2:python manage.py migrate
### 3:python manage.py runserver 0.0.0.0:8000
### 4:python manage.py startapp polls
### 5:python manage.py makemigrations polls 
\[polls/migrations 目录下生成\] <br/>
### 6:python manage.py sqlmigrate polls 0001 
\[查看建表SQL\]<br/>
### 7:python manage.py migrate 
\[创建polls对应表\]<br/>
### 8:python manage.py shell
\[加载django环境的交互界面,<br/>
manage.py sets the DJANGO\_SETTINGS\_MODULE environment variable, <br/>
which gives Django the Python import path to your mysite/settings.py file.\]<br/>
[[Once you’re in the shell, explore the database API:](https://docs.djangoproject.com/en/1.8/topics/db/queries/)]<br/>
[[Accessing related objects](https://docs.djangoproject.com/en/1.8/ref/models/relations/)]<br/>
### 9:python manage.py createsuperuser 
\[pwd 848\]<br/>

> mysite/
> 
> > manage.py [[detail](https://docs.djangoproject.com/en/1.8/ref/django-admin/)]
>
> > mysite/
>
> > > \_\_init\_\_.py
>
> > > settings.py [[detail](https://docs.djangoproject.com/en/1.8/topics/settings/)]
>
> > > urls.py [[detail](https://docs.djangoproject.com/en/1.8/topics/http/urls/)]
>
> > > wsgi.py [[How to deploy with WSGI](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/)]

### test
>
> 测试time\_zone相关设置
>
> django 环境model相关导入
>
> \# todo ? django_admin_log 是否可以自定义
>
> tips \[Writing your first Django app, part 2\] # todo [The Django admin site](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)
>
> > 重新定制admin后台页面 模板(拷贝对应模板到 settings中 TEMPLATES DIRS目录下，修改即可)
>
> > > python -c "import sys;sys.path = sys.path[1:];import django;print(django.\_\_path\_\_)" # 查看django安装路径
>
> \[url # todo 如果url(name参数内容重复会怎样?) [django.core.urlresolvers](https://docs.djangoproject.com/en/1.8/ref/urlresolvers/#module-django.core.urlresolvers)]
>
> \[# todo [Django shortcut functions](https://docs.djangoproject.com/en/1.8/topics/http/shortcuts/#module-django.shortcuts)\]
>
> \[# todo detail of [csrf](https://docs.djangoproject.com/en/1.8/ref/csrf/)\]
>
> \[# todo [Request and response objects](https://docs.djangoproject.com/en/1.8/ref/request-response/)\]
>
> 利用generic views的例子,利用了一套新的url测试(polls\_generic)
>
> > \[# todo 快速list,detail模型 [Generic display views](https://docs.djangoproject.com/en/1.8/ref/class-based-views/generic-display/) [Class-based views](https://docs.djangoproject.com/en/1.8/topics/class-based-views/)\]
>
> 静态文件处理方法参考[Managing static files (CSS, images)](https://docs.djangoproject.com/en/1.8/howto/static-files/)<br/>
[Deploying static files](https://docs.djangoproject.com/en/1.8/howto/static-files/deployment/)<br/>
[The staticfiles app](https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/)<br/>
> \[[文件处理：Managing files](https://docs.djangoproject.com/en/1.8/topics/files/)]\]

#### MEDIA\_ROOT 相关设置想法
    
    之前想每一个APP，使用自己的一套上传文件文件夹（放在自己APP目录里面的media里面通过inspect获得了APP的绝对路径）
    主settings.py里面
    1、MEDIA_URL = '/media/'
    2、APP对应路径下，model中指定了FileSystemStorage
    3、在自己的APP里面的url里面添加了
    urlpatterns += static(settings.MEDIA_URL, document_root = APP_UPLOAD_DIR)
    # 这样的问题就是图片的访问路径会有问题
    # self.pic.url = '/media/QuestionPic/2015/06/06/113.pic.jpg'
    # 但是 实际图片可以访问的地址是：
    # http://127.0.0.1:8000/questions/media/QuestionPic/2015/06/06/113.pic_un70WY7.jpg
    # 就算我把 3、放入到整体的settings中，document_root 也不能做到指定到多个地方

改变了思想，将所有的app都指向同一个MEDIA\_ROOT,在**upload\_to**中多添加app的名字





