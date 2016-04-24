from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
# import models
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# from recharge_panel.config import logging
import traceback

# Create your views here.


@csrf_exempt
def login(request):

    format = "%a %b %d %H:%M:%S %Y"
    today = datetime.datetime.now()
    login_date = today.strftime(format)
    try:
        if request.method == 'POST':
                # script_log.debug("Post Request "+str(request.get_host()))
                # script_log.debug("Post Request for User "+request.POST['username'])
                username = request.POST['username']
                password = request.POST['password']
                request.session.set_expiry(2000)
                if username == 'admin' and password == 'admin' :
                        #cache.set('get_data',None)
                        request.session['role'] = 'user'
                        request.session['username']= username
                        request.session['last_login'] =  login_date
                        main_data = [] #get_data.data({'query':'summary_data'},script_log)
                        #request.session['detail_data'] = main_data
                        context_data = {'modal_url':'/view_details/','main_content':'summary.html','key':'summary','body_template': 'dashboard/dashboard.html'}
                        context = RequestContext(request,context_data)
                        
                        return HttpResponseRedirect('/dashboard')
                        # template = loader.get_template("commons/index.html")
                        #
                        # return HttpResponse(template.render(context))
                else:

                    request.session.flush()
                    return render(request,'login/login.html',context={'error':"true"})
        else:

            if (request.session.__contains__('username')):
                    request.session.set_expiry(2000)

                    main_data = [] #get_data.data({'query':'summary_data'},script_log)

                    context_data = {'modal_url':'/view_details/','main_content':'summary.html','key':'summary','body_template': 'dashboard/dashboard.html'}

                    context = RequestContext(request,context_data)

                    return HttpResponseRedirect('/dashboard')
                    # template = loader.get_template("commons/index.html")
                    # return HttpResponse(template.render(context))

        return render(request,'login/login.html')
    except Exception as exc:
        print exc
        # script_log.warn("Error "+str(exc.message))
        # script_log.error("Error"+str(traceback.format_exc()))
        return render(request,'commons/login.html')



def index(request):
    request.session.set_expiry(3600)
    context_data = RequestContext(request,
                                  {'body_template': 'dashboard/dashboard.html',"aUrl":"/recharge_view_plan",
                                   'session_data': request.session, "success": "false", "error": "error",
                                   })
    request.session['role'] = 'user'
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')