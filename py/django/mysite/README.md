基本流程
---------
### 1:django-admin startproject mysite (version 1.8.1)
### 2:python manage.py migrate
### 3:python manage.py runserver 0.0.0.0:8000
### 4:python manage.py startapp polls
### 5:python manage.py makemigrations polls \[polls/migrations 目录下生成\]
### 6:python manage.py sqlmigrate polls 0001 \[查看建表SQL\]
### 7:python manage.py migrate \[创建polls对应表\]
### 8:python manage.py shell
\[加载django环境的交互界面,manage.py sets the DJANGO\_SETTINGS\_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file.\]<br/>
[[Once you’re in the shell, explore the database API:](https://docs.djangoproject.com/en/1.8/topics/db/queries/)]<br/>
[[Accessing related objects](https://docs.djangoproject.com/en/1.8/ref/models/relations/)]<br/>
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
