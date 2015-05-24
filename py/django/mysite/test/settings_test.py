#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import sys
sys.path.append("../")

from django.conf import settings
from mysite import settings as app_settings

settings.configure(default_settings = app_settings ,DEBUG = True)

def test_time_zone_settings():
    """ 
        settings TIME_ZONE & USE_TZ test
        
        (1)
        TIME_ZONE = 'UTC'
        USE_TZ = True
        print : [UTC] : 2015-05-24 08:29:49.930913+00:00
        (2)
        TIME_ZONE = 'UTC'
        USE_TZ = False
        print : [UTC] : 2015-05-24 16:32:36.105646
        (3) (就用这个)
        TIME_ZONE = 'Asia/Shanghai'
        USE_TZ = False
        print : [Asia/Shanghai] : 2015-05-24 16:33:30.352510 
        (4)
        TIME_ZONE = 'Asia/Shanghai'
        USE_TZ = True
        print : [Asia/Shanghai] : 2015-05-24 08:34:23.357575+00:00

        # refer: https://docs.djangoproject.com/en/1.8/topics/i18n/timezones/
    """
    from django.utils import timezone
    now = timezone.now()
    print type(now) # <type 'datetime.datetime'>
    print "[%s] : %s" % (settings.TIME_ZONE, now)


if __name__ == "__main__":
    test_time_zone_settings()
