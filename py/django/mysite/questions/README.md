Models 学习
===================================
[Model syntax](https://docs.djangoproject.com/en/1.8/topics/db/models/)
### 一些查询(对应model.py内容)
    p = Paper.objects.get(pk = 1)
    q = Question.objects.get(pk =1)
    r = PaperQuestionRelation(paper = p, questions = q ,user_answer = "A",score = 10)
    r.save()
    p.questions.all() # 
    q.papers.all() #q.paper_set.all() # 默认 若果没有# tips 1
    # That's now the name of the reverse filter# tips 2
    QuestionUser.objects.filter(paper__title = "TEST (2015-06-03)")  

    清除paper 和 question 之间的关联
    q = Question.objects.get(pk = 1)
    q.papers.clear()

### 调试
打印出SQL
    
    queryset = Paper.objects.filter(questions__type = 'SC',question_relations__seq_num = 1)
    print queryset.query
    SELECT `questions_paper`.`id`, `questions_paper`.`title`, 
        `questions_paper`.`user_id`, `questions_paper`.`create_time`, `questions_paper`.`update_time` 
    FROM `questions_paper` INNER JOIN `questions_paperquestionrelation` ON 
    ( `questions_paper`.`id` = `questions_paperquestionrelation`.`paper_id` ) INNER JOIN `questions_question` ON 
    ( `questions_paperquestionrelation`.`question_id` = `questions_question`.`id` ) WHERE 
    (`questions_paperquestionrelation`.`seq_num` = 1 AND `questions_question`.`type` = SC)

###  todo
> 字段属性
> > GenericIPAddressField
>

### 引出相关问题
\[Meta : [Model Meta options](https://docs.djangoproject.com/en/1.8/ref/models/options/)\] <br />
\[直接执行SQL ：[Performing raw SQL queries](https://docs.djangoproject.com/en/1.8/topics/db/sql/)\]<br/>
\[模型方法, 重写 : [Model instance reference](https://docs.djangoproject.com/en/1.8/ref/models/instances/)\]<br/>
\[模型的关系, 多对多中间模型会导致一些方法失效 [Related objects reference](https://docs.djangoproject.com/en/1.8/ref/models/relations/)\]<br/>
\[[One-to-one relationships](https://docs.djangoproject.com/en/1.8/topics/db/examples/one_to_one/)\]<br/>
\[[Many-to-one relationships](https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_one/)\]<br/>
\[[Many-to-many relationships](https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/)\]<br/>


### 重载save方法
```
    
    from django.db import models
    
    class Blog(models.Model):
        name = models.CharField(max_length=100)
        tagline = models.TextField()
        
        def save(self, *args, **kwargs):
        do_something()
        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
        do_something_else()
```

Overridden model methods are not called on bulk operations 
Note that the **delete()** method for an object is not necessarily called when [deleting objects in bulk using a QuerySet](https://docs.djangoproject.com/en/1.8/topics/db/queries/#topics-db-queries-delete). 
To ensure customized delete logic gets executed, 
you can use **pre_delete** and/or **post_delete** signals.
Unfortunately, there isn’t a workaround when **creating** or **updating** objects in bulk, since none of **save()**, **pre_save**, and **post_save** are called.<br/>

#### tips
* ImageField 在admin界面中，删除不会删除文件系统中的文件，只是删除了数据库中path
```    
    a = QuestionPic.objects.get(pk = 3)
    a.pic.delete()
    #会删除文件，并且update数据库字段，将ImageField那个字段置空
    a.pic.delete(save = False)
    #会删除文件，并且update数据库字段，但ImageField那个字段没做操作
```

