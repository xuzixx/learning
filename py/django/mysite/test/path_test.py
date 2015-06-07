import os
import inspect


print os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
