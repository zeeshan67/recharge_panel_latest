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
    context_data = RequestContext(request,
                                  {'body_template': 'dashboard/dashboard.html',"aUrl":"/get_recharge_counts",
                                   'session_data': request.session, "success": "false", "error": "error",
                                   })
    request.session['role'] = 'user'
    main_data = get_data({"query":"dashboard_data"})
    context_data['total_success'] = main_data['total_success']
    context_data['total_recharge'] = main_data['total_count']
    context_data['total_balance']  = 900
    print context_data
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))

