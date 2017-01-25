from django.http import HttpResponse
from django.template import loader

# http://stackoverflow.com/a/11158224
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import main

def page(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render({},request))
