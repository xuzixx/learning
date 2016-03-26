# Application

> Main Name
> Configuration 配置
> Laziness
> Breaking the chain
> Abstract Tasks


Celery 库使用前必须先实例化，这个实例可以称为application或者简称app

这个app 是线程安全的，所以多个不同配置、不同组件（components）、不太任务（tasks）Celery 的applications 可以共同存在于一个进程空间

```
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```
最后一行显示的是文本状态的这个app，包含类名（Celery）、当前main module（\_\_main\_\_）、内存地址（0x100469fd0）

## Main Name
这部分只有main module name 是重要的

当我们在Celery 中发送一个task message, 这个message 只有你想要执行的这个task 的名字，然而并不会含有任何源代码。每一个worker 包含一个task names 和真实执行的方法的对应关系，我们称为 任务注册表（task registry）

每当我们定义一个task，这个task 就会被加入到本地注册表（local registry）

```
>>> @app.task
... def add(x, y):
...     return x + y

>>> add
<@task: __main__.add>

>>> add.name
__main__.add

>>> app.tasks['__main__.add']
<@task: __main__.add>
```

在这里我们油看到了 \_\_main\_\_，每当Celery 不能查明这个方法属于哪个module 的时候，Celery就用 main module name 来生成task 名字的开头.

这样会在有些应用情况下有问题：
1. 如果task 定义在的这个module作为一个程序在运行
2. 如果这个应用是被python shell(REPL)创建的

如下例子，tasks module 通过app.worker\_main()来去启动一个worker:

tasks.py:

```
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()
```
当这个module 执行的时候，tasks 将会被以 “\_\_main\_\_”命名，但是当module被别的process import入的时候，tasks 的名字就是以“tasks”开头（真实的module名字）
```
>>> from tasks import add
>>> add.name
tasks.add
```

可以给main module指定一个特定的名字：
```
>>> app = Celery('tasks')
>>> app.main
'tasks'

>>> @app.task
... def add(x, y):
...     return x + y

>>> add.name
tasks.add
```

#### 相关：Names
## Configuration 配置

有好多可选的配置来改变Celery。这些配置可以直接在在app 实例创建的时候设置，也可以通过配置模块来配置

配置可以通过app.conf 查看：
```
>>> app.conf.CELERY_TIMEZONE
'Europe/London'
```
在app.conf 中也可以直接配置：
```
>>> app.conf.CELERY_ENABLE_UTC = True
```
也可以通过update 方法更新多个配置参数（keys）
```
>>> app.conf.update(
...     CELERY_ENABLE_UTC=True,
...     CELERY_TIMEZONE='Europe/London',
...)
```
configuration 对象内容的变化的优先级：
1. 在运行期间改变
2. configuration 模块（如果有）
3. 默认的configuration (celery.app.defaults)
也可以添加新的default 通过app.add\_defaults() 方法
#### 相关：Configuration reference 有完整的配置列表和默认值

### config\_from\_object
app.config\_from\_object() 方法从配置对象中加载配置
注意任何在config\_from\_object() 之前的配置将会被重置，所以一些额外的配置需要在这个方法后。

#### Example 1: Using the name of a module
```
from celery import Celery

app = Celery()
app.config_from_object('celeryconfig')
```
celeryconfig 模块如下：
celeryconfig.py:
```
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/London'
```
#### Example 2: Using a configuration module
> Tips:
> Using the name of a module is recomended as this means that the module doesn’t need to be serialized when the prefork pool is used. If you’re experiencing configuration pickle errors then please try using the name of a module instead.
```
from celery import Celery

app = Celery()
import celeryconfig
app.config_from_object(celeryconfig)
```
#### Example 3: Using a configuration class/object
```
from celery import Celery

app = Celery()

class Config:
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'Europe/London'

app.config_from_object(Config)
# or using the fully qualified name of the object:
#   app.config_from_object('module:Config')vkk
```
### config\_from\_envvar
app.conf\_from\_envvar() 从环境变量中获取configuration module的名字

例如 加载configuration 从一个环境变量中叫CELERY\_CONFIG\_MODULE 的module:
```
import os
from celery import Celery
#: Set default configuration module name
os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
```
可以指名configuration module 通过启动环境：
```
$ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l info
```
### Censored configuration 审查配置
如果你想要作为debug 信息打印出配置，你可能也想滤出类似密码和API keys之类的信息
Celery 有一些组件用来展示configuration，其中一个是 humanize():
```
>>> app.conf.humanize(with_defaults=False, censored=True)
```
这个方法返回列表展示的configuration。返回结果只会包含和default 不同的配置，但是也可以通过改变 with\_defaults 参数来显示默认的配置

如果你想用字典类型查看configuration，可以使用table() 方法：
```
>>> app.conf.table(with_defaults=False, censored=True)
```
请注意Celery 不会过滤掉所有的敏感信息，Celery 只是通过正则简单匹配。如果添加了自定义的敏感信息的配置，应该使用Celery 明确的安全标识。
如果配置中的key包含如下字符串，Celery 将会滤掉：
API, TOKEN, KEY, SECRET, PASS, SIGNATURE, DATABASE

## Laziness
app 实例是lazy 的，只有真的要做什么事情的时候才有所作为
创建Celery 实例只做了如下事情：
1. 创建了一个逻辑时钟实例，给events 使用
2. 创建了任务注册表（task registry）
3. 将自己这个实例作为当前的app(但是如果set\_as\_current 参数设置disabled也不作为)
4. 调用app.on\_init() 这个callback（这个默认什么也不做）

当app.taks() 这个装饰器被调用的时候，其实还没有没有创建tasks，创建这个task 的时间会被推迟到这个task 被使用，或者 在这个app被确定（after the application has been finalized）

下面这个例子会说明task 直到你使用或访问其中的属性（这个例子中 repr()）才被创建:
```
>>> @app.task
>>> def add(x, y):
...    return x + y

>>> type(add)
<class 'celery.local.PromiseProxy'>

>>> add.__evaluated__()
False

>>> add        # <-- causes repr(add) to happen
<@task: __main__.add>

>>> add.__evaluated__()
True
```
app 的Finalization 发生在 app.finalize() 被明确调用，或者 隐式访问 app.tasks 的属性

明确这个对象将会(Finalizing)：
1. 复制被apps共享的tasks 
> 默认所有的tasks 都是被共享的。但是装饰器里面 shared 参数disabled，这个task 将会绑定成这个app 私有的
2. 评估所有的将要发生的tasks 装饰器
3. 确保所有的tasks 将会绑定到当前app
> tasks 被绑定到apps 中，所以它可以读取默认的配置

#### default app
Celery 并不总是这么工作的，他过去只有一个module-based API，并且为了向前兼容性，老的API 依然保留。
Celery 总是创建一个特定的app，就是default app，如果没有用户的app(custom app)被创建，这个app 将会被使用。
celery.task 模块在这里是为了兼容老的API，如果你定义了一个用户app（custom app）这个模块并不应该使用。应该使用app 实例的方法，不是module 中基础的API。
例如，老的old task base class 使用了好多兼容特性,这些会和新特性有冲突。例如task methods：
```
from celery.task import Task   # << OLD Task base class.
from celery import Task        # << NEW base class.
```
即使你使用老的module-based API，也推荐使用新的基类（base class）
## Breaking the chain
大多数情况下都是依赖被设定的当前的app，所以最佳实践是 将app 实例传入所有需要它的地方

这样就创造了一个依赖app 实例的链条，我们叫这个app chain，

下面是*不好的*：
```
from celery import current_app

class Scheduler(object):

    def run(self):
        app = current_app
```
我们应该用app 作为参数传入：
```
class Scheduler(object):

    def __init__(self, app):
        self.app = app
```
在Celery 内部使用celery.app.app\_or\_default()方法来保证在module-based API中也兼容使用
```
from celery.app import app_or_default

class Scheduler(object):
    def __init__(self, app=None):
        self.app = app_or_default(app)
```
在*开发模式*中可以设置CELERY\_TRACE\_APP 环境变量，来抛出app chain break的异常：
```
$ CELERY_TRACE_APP=1 celery worker -l info
```
#### Evolving the API
Celery 从最初创建到现在已经变化了很多
例如，最开始可以使用任何可以调用的方法最为task：
```
def hello(to):
    return 'hello {0}'.format(to)

>>> from celery.execute import apply_async

>>> apply_async(hello, ('world!', ))
```
你也可以创建一个Task 类来设置一些必须项或者重载一些方法
```
from celery.task import Task
from celery.registry import tasks

class Hello(Task):
    send_error_emails = True

    def run(self, to):
        return 'hello {0}'.format(to)
tasks.register(Hello)

>>> Hello.delay('world!')
```
后来，由于使用除了pickle 外的序列化非常困难，2.0中移除了了这个特性，使用装饰器作为代替
```
from celery.task import task

@task(send_error_emails=True)
def hello(x):
    return 'hello {0}'.format(to)
```

## Abstract Tasks
所有通过 task() 装饰器声明的task 都会继承Task 基类
可以通过base 参数指定别的基类
```
@app.task(base=OtherTask):
def add(x, y):
    return x + y
```
创建一个用户自定义的task 类需要继承 中间的基类(neutral base class)：
*celery.Task.*
```
from celery import Task

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)
```
> Tips:
如果你重载了 Task 的 \_\_call\_\_ 方法，那么也必须调用super 的\_\_call\_\_ 以确保当一个task 被直接调用，base call method 可以建立默认的 request used

中间的基类（neutral base class）因为不绑定在任何指定的app中，所以是特别的。
这个类的子类的实类将会被绑定,所以要是还是普通继承base class 需要标识出abstract
一旦一个任务绑定到app ，它将会读取configuration 来设置默认值等等。

可以通过改变默认的基类通过改变app.Task() 属性
```
>>> from celery import Celery, Task

>>> app = Celery()

>>> class MyBaseTask(Task):
...    abstract = True
...    send_error_emails = True

>>> app.Task = MyBaseTask
>>> app.Task
<unbound MyBaseTask>

>>> @app.task
... def add(x, y):
...     return x + y

>>> add
<@task: __main__.add>

>>> add.__class__.mro()
[<class add of <Celery __main__:0x1012b4410>>,
 <unbound MyBaseTask>,
 <unbound Task>,
 <type 'object'>]
```

















