from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
# from recharge_panel.config import logging
import traceback,json
from recharge_panel_app.forms import campaign_form
from recharge_panel_templates.config import operator_code_dict,post_url


def create_recharge_mobile(request):
    url = "/create_recharge_mobile/"
    message = ''
    # user_id = request.session['user_id']
    # scripts = user_master.get_scripts(user_id)
    script_list = []
    new_camp_form = campaign_form.CreateCampaignForm()

    # for script in scripts['script_details']:
    # script_list.append(script['script_name'])

    context_data = RequestContext(request,
                                  {'body_template': 'campaign/create_recharge_mobile.html', 'aUrl': url,
                                   'session_data': request.session, "success": "false", "error": "false",
                                   "scripts": script_list})
    try:
        context_data['form'] = new_camp_form
        if request.method == "POST":

            new_camp_form = campaign_form.CreateCampaignForm(request.POST)


            if new_camp_form.is_valid():
                mobile_number = request.POST['mobile_number']
                circle = request.POST['circle']
                operator = request.POST['operator']
                amount = request.POST['amount']
                recharge_type = request.POST['recharge_type']
                credit_used = request.session['credit_used']
                credit_available = request.session['credit_available']
                print amount,credit_used,credit_available
                if float(amount) <= float(credit_available-credit_used):
                    api_params = {"mobile_number":mobile_number,"circle":circle,"recharge_type":recharge_type,
                                  "amount":amount,"operator_code":operator_code_dict['%s_%s'%(operator,recharge_type)],
                                  "username":request.session['username'],"user_id":request.session['user_id'],"credit_available":credit_available,"credit_used":credit_used
                                  }
                    print api_params
                    response = requests.post(post_url, json=api_params)
                    print response.text
                    context_data['success'] = "true"
                    message = "Recharge request successfully sent."
                else:
                    message = "Don't have enough credits."
                    context_data['error'] = "true"
            else:
                context_data['form'] = new_camp_form
        context_data['message'] = message

    except Exception as e:
        print "Exception %s"%e.message
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))

