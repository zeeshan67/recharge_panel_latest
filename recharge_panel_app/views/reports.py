__author__ = 'verna'
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
import traceback,json


def get_report(request):
    request.session.set_expiry(3600)
    context_data = RequestContext(request,
                                  {'body_template': 'reports/reports.html',"aUrl":"/recharge_view_plan",
                                   'session_data': request.session, "success": "false", "error": "error",
                                   })
    # request.session['role'] = 'user'
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))


@csrf_exempt
def recharge_data(request):
    try:
        from_date = request.POST.get('startDate',False)
        to_date = request.POST.get('endDate',False)
        display_start = request.POST.get('iDisplayStart',False)
        display_end = request.POST.get('iDisplayLength',False)
        search = request.POST.get('sSearch', '.*')
        event_start_date = event_end_date = ''
        if from_date:
            event_start_date = str(from_date.split('/')[2])+'-'+str(from_date.split('/')[0])+"-"+str(from_date.split('/')[1])
        if to_date:
            event_end_date = str(to_date.split('/')[2])+"-"+str(to_date.split('/')[0])+"-"+str(to_date.split('/')[1])
        display_content = []
        total_count = 0

        print "start date %s"%display_start

        if request.is_ajax() or request.method == 'POST':
                    main_data = get_data({'user_id':request.session['user_id'],'user_role':request.session['role'],'query':'recharge_data','event_start_date':event_start_date,
                                               'event_end_date':event_end_date,'limit':display_end,
                                               'offset':display_start,'search':search})
                    if isinstance(main_data,dict):
                        display_content = main_data['final_data']
                        total_count = main_data['total_count']
                    context_data = {'modal_url':'/view_details/','main_content':'main_data.html','key':'detailed','display_content':display_content}
                    context = RequestContext(request,context_data)

                    # template = loader.get_template("main_data.html")
                    response = dict(set=0, sEcho=request.POST['sEcho'], iTotalRecords=total_count, iTotalDisplayRecords=total_count,
                                        aaData=display_content)
                    return HttpResponse(json.dumps(response))

    except Exception as exc:
            print("Error "+str(traceback.format_exc()))
