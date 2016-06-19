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
from recharge_panel_app.models import verify_user
from recharge_panel_templates.config import operator_code_dict,post_url

# from recharge_panel.config import logging
import traceback,json

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
                username = username.strip(' ')
                password = password.strip(' ')
                password = hashlib.md5(request.POST['password']).hexdigest()
                user_params = {"username":username,"password":password}
                verification_result = verify_user(**user_params)
                print verification_result
                if verification_result['is_verified'] :
                        request.session.set_expiry(2000)
                        credit_used = verification_result.get("credit_used",0)
                        credit_available = verification_result.get("credit_available",0)
                        request.session['credit_used'] = credit_used
                        request.session['user_id'] = verification_result.get("user_id",0)
                        request.session['parent_id'] = verification_result.get("parent_id",0)
                        request.session['credit_available'] = credit_available
                        #cache.set('get_data',None)
                        request.session['role'] = verification_result.get('role','guest')
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
        return render(request,'login/login.html')

@csrf_exempt
def mobile_app_authenticate(request):
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        username = username.strip(' ')
        password = password.strip(' ')
        password = hashlib.md5(request.POST['password']).hexdigest()
        user_params = {"username":username,"password":password}
        verification_result = verify_user(**user_params)
        if verification_result['is_verified']:
            print(verification_result['credit_used'])
            print(verification_result['credit_available'])
            response ={"code":200,"msg":"Login Successful","user_id":verification_result["user_id"]}
            return HttpResponse(json.dumps(response))
    response = response ={"code":401,"msg":"Invalid Credentials"}
    return  HttpResponse(json.dumps(response))


@csrf_exempt
def create_mobile_recharge(request):
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        mobile_number = request.POST.get('mobile_number')
        username = username.strip(' ')
        password = password.strip(' ')
        password = hashlib.md5(request.POST['password']).hexdigest()
        user_params = {"username":username,"password":password}
        circle = request.POST.get("circle",None)
        operator_code = request.POST.get("operator_code","")
        recharge_type = request.POST.get("recharge_type","prepaid")
        user_id = request.POST.get("user_id",None)
        verification_result = verify_user(**user_params)
        if verification_result['is_verified']:
            amount = request.POST.get("amount",None)
            context_data = {"code":200}
            if float(amount) <= float(verification_result['credit_available']):
                    api_params = {"mobile_number":mobile_number,"circle":circle,"recharge_type":recharge_type,
                                  "amount":amount,"operator_code":operator_code,
                                  "username":username,"user_id":user_id,"credit_available":verification_result['credit_available'],"credit_used":verification_result['credit_used']
                                  }
                    try:
                        response = requests.post(post_url, json=api_params)
                        print response.text
                        api_response = eval(str(response.text))
                        return  HttpResponse(json.dumps(api_response))
                    except Exception as exc:
                        print "eror %s"%exc.message
                        context_data.update({'recharge_status':"FAILED","remark":"Error while doing recharge,please contact admin.","request_id":""})
                        return  HttpResponse(json.dumps(context_data))
            else:
                context_data.update({'success':0})
                context_data.update({'msg':"Don't have enough credits."})
                return  HttpResponse(json.dumps(context_data))
    response = response ={"status_code":401,"msg":"Invalid Credentials"}
    return  HttpResponse(json.dumps(response))

def index(request):
    request.session.set_expiry(3600)
    context_data = RequestContext(request,
                                  {'body_template': 'dashboard/dashboard.html',"aUrl":"/recharge_view_plan",
                                   'session_data': request.session, "success": "false", "error": "error",
                                   })
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))




def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')


