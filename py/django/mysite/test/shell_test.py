#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import sys, os
sys.path.append("../")

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

def test_script_with_django_api():
    """
        (1)
            Now, let’s hop into the interactive Python shell 
            and play around with the free API Django gives you.
            To invoke the Python shell, use this command:
            python manage.py shell
        (2)
            as follows
    """
    import django
    django.setup()

    from polls.models import Question, Choice
    q = Question.objects.get(id = 1)
    print Question.objects.all()
    print type(q.question_text)
    print q.question_text

if __name__ == "__main__":
    test_script_with_django_api()

