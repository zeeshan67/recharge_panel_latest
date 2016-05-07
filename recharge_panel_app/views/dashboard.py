from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
from recharge_panel_app.models import get_data
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# from recharge_panel.config import logging
import traceback

# Create your views here.





def index(request):
    request.session.set_expiry(3600)
    user_id = request.session.get('user_id',0)
    context_data = RequestContext(request,
                                  {'body_template': 'dashboard/dashboard.html',"aUrl":"/get_recharge_counts",
                                   'session_data': request.session, "success": "false", "error": "error",
                                   })
    # request.session['role'] = 'admin'
    main_data = get_data({"query":"dashboard_data","user_id":user_id,"parent_id":request.session.get('parent_id',None),"user_role":request.session.get('role',None)})
    context_data['total_success'] = main_data['total_success']
    context_data['total_recharge'] = main_data['total_count']
    context_data['total_balance']  = main_data['total_balance']
    context_data['total_credit']  = main_data['total_credit']
    print context_data
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))

