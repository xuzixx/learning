# Tasks

Tasks 是Celery 应用的基石

一个taks 是一个class，只要能被调用就行。它有双重角色表现在它定义了 (1)当一个task被调用（sends a message）做什么操作，(2)当一个worker 接收到这个那个消息做什么

每一个task class都有唯一的名字，这个名字会在message 中提到以确保worker 可以找到正确的方法去执行

一个task message 在被一个worker[认领(acknowledged)]()前不会消失。一个worker 可以预先保留多个message 即使这个worker 被杀掉,这个message 也会被重新分配给别的worker

理想的task 方法应该是[idempotent](),意思是这个方法即使被以同样的参数多次调用也不会引起不明确的影响。由于worker 不能查明task 是否idempotent,所以默认的处理方式是 在执行之前预先先认领这个message，所以一个task 如果已经开始执行，那么就不会重复执行

如果task 是idempotent ，可以设置 acks\_late 选项，让worker 认领这个message 在task 返回后。也可查看相关FAQ[Shoud I use retry or acks\_late?]()

在这个章节价格会看到关于定义task，下面是目录：
> Basics
> Names
> Context
> Logging
> Retrying
> List of Options
> Status
> Semipredicates
> Custom task classes
> How it works
> Tips and Best Practices
> Performance and Strategies
> Example
## Basics 基础
可以使用task() 装饰器来创建一个task：
```
from .models import User

@app.task
def create_user(username, password):
    User.objects.create(username=username, password=password)
```
这里有好多[选项]()可以为这个task 设置，通过装饰器中指明参数即可：
```
@app.task(serializer='json')
def create_user(username, password):
    User.objects.create(username=username, password=password)
```

> Tips
> 多个装饰器,如下
```
@app.task
@decorator2
@decorator1
def add(x, y):
    return x + y
```
> 如何引入task 装饰器
> 如果使用Django 或者 依然使用老的 module-based API,如下
```
from celery import task

@task
def add(x, y):
    return x + y
```
## Names
每一个task 必须有一个唯一的name，如果没有用户自定义的名字就会根据方法名字生成一个
如下：
```
>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'
```
最佳实践是 使用模块模子作为命名空间，这样名字不会和别的模块发生冲突
```
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y
```
这将生成一个在哪里都是明确的名字，如果module 名字是"tasks.py":
tasks.py:
```
@app.task
def add(x, y):
    return x + y

>>> from tasks import add
>>> add.name
'tasks.add'
```
### 自动的命名 和 相对引入（automatic naming and relative imports）
relative imports 和 automatic name 是相互冲突的，所以如果你使用relative imports，那么你就需要明确的设置name

例如client 利用".tasks"形式引入模块"myapp.tasks"，worker 使用"myapp.tasks",上面生成的名称将不匹配，worker 会抛出一个*NotRegistered* 错误

这个问题也会发生在Django 和 使用INSTALLED\_APPS (project.myapp 这种风格):
```
INSTALLED_APPS = ['project.myapp']
```
如果应用这个app 在project.myapp 这个名称下，那么task module 需要像 project.myapp.tasks 引入，需要确保每次import task 都是一样的：
```
>>> from project.myapp.tasks import mytask   # << GOOD

>>> from myapp.tasks import mytask    # << BAD!!!
```
第二个例子由于worker 和client 用不同的名字引入模块，将会导致这个task 有不同的名字
```
>>> from project.myapp.tasks import mytask
>>> mytask.name
'project.myapp.tasks.mytask'

>>> from myapp.tasks import mytask
>>> mytask.name
'myapp.tasks.mytask'
``` 
由于以上的原因，你必须考虑怎么引入模块，这也是Python最佳实践。
同样也不要使用老式的 相对引入：
```
from module import foo   # BAD!

from proj.module import foo  # GOOD!
```
新式的相对引入是好的：
```
from .module import foo  # GOOD!
```
当工程中已经大量混乱使用，也没有时间去更正的话，最好使用明确的名称来代替automatic naming:
```
@task(name='proj.tasks.add')
def add(x, y):
    return x + y
```
## Context 内容
[request]() 包含执行的task 的相关信息和状态
request 定义了如下相关的属性：
id: task 执行的唯一ID
group: 如果task 是group 的一个成员,返回group 的id
chord: 这个task 属于的chord 的唯一id（如果task 是header 的一部分）
args: Positional arguments.
kwargs: Keyword arguments.
reties: 当前任务将被重试的次数。需要一个从0开始的整数
is\_eager: 如果这个task 将被client 本地执行，而不是worker，则设置为*True*
eta: task 原始的ETA(如果存在).这是一个UTC 时间（依赖CELERY\_ENABLE\_UTC 设置）
expires: task 原始的超时时间(如果存在).这是一个UTC 时间（依赖CELERY\_ENABLE\_UTC 设置）
logfile: worker 的日志文件. 相关[Logging]()
loglevel: 当前日志的级别
hostname: 执行这个task 的worker 实例的hostname
delivery\_info: 额外的分发信息.这是一个mapping 包含了用于分发这个task的exchange 和routing key。例如可以被 retry() 重新发送这个task 到同样的目标queue。这个字典的可用关键字keys 依赖于使用的message broker
called\_directly: 如果这个task 不被worker 执行，那么这个标识 设置为True 
callbacks: 如果这个task 返回successfully, 被调用的subtasks 的*列表*
errback: 如果这个task 失败，被调用的subtasks 的*列表*
utc: Set to true the caller has utc enabled (CELERY\_ENABLE\_UTC).
**3.1 新特性**
headers: Mapping of message headers(可能是None)
reply\_to: 发送答复的地方（queue 名称）
correlation\_id: 通常和task id 相同，总是用在amqp 来追踪一个回复（reply）的源头

一个获取相关信息的示例task
```
@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))
```
bind 参数表示这个方法将会是一个"bound method"，因此可以通过task type 实例获取属性和方法

## Loggin 日志
worker 将会自动建立logging，也可以人工配置logging

一个叫"celery.task"的logger 是可以使用的，你可以继承这个logger 来自动获取task 的名字 唯一id 
创建一个通用logger 的最佳实践是 在所有task 之前创建一个common logger
```
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```
Celery 使用标准的Python logger 库，可以在[logging]() 模块看相关文档

如果你使用print() 作为标准输出/标准错误 将会重定向到logging 系统中（可以通过CELERY\_REDIRECT\_STDOUTS 设置关闭）

> Note：
> 











