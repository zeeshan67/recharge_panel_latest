from django.template import RequestContext, loader
from django.http import HttpResponse,Http404
# from recharge_panel_app.forms import user_form
# from recharge_panel_app.models import CreateUser
# import hashlib
from recharge_panel_app.models import CreateUser
from django.views.decorators.csrf import csrf_exempt
from recharge_panel_app.models import CreateUser,get_user_name,get_user_credits
from recharge_panel_app.forms import user_form
import json
def view_user(request):
    role = request.session['role']
    context_data = RequestContext(request,
                                  {'body_template': 'user/view_user.html',
                                   'session_data': request.session,
                                   "success": "false",
                                   "error": "error"})
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))

@csrf_exempt
def get_user_data(request):
    if request.method == 'POST' and not request.POST.__contains__('modal_use'):
        try:
            display_start = request.POST.get('iDisplayStart',False)
            display_end = request.POST.get('iDisplayLength',False)
            search = request.POST.get('sSearch', '.*')
            search_param = {}
            if request.session['role'] == 'distributor':
                search_param = {"parent_id":int(request.session['user_id'])}
            if search:
                if search.isdigit():
                    search_param.update({"mobile_number__icontains":str(search)})
                else:
                    search_param.update({"user_name__icontains":str(search)})
            total_data = CreateUser.objects.filter(**search_param).count()
            main_data = CreateUser.objects.filter(**search_param)[int(display_start):int(display_end)]
            user_data = []
            for values in main_data:
                #,
                query_param = {"parent_id":values.parent_id}
                parent_user_data  = get_user_name(query_param)
                user_data.append({"user_name":values.user_name,"email_id":values.email_id,"mobile_number":values.mobile_number,
                                 "credit_available":str(values.credit_available) if values.credit_available else 0,"credit_used":str(values.credit_used)
                    if values.credit_used else 0,
                                 "credit_assigned":str(values.credit_assigned),"user_role":values.user_role,"user_id":values.id,
                                 "parent_id":parent_user_data['user_name']
                                  })
            response = dict(set=0, sEcho=request.POST['sEcho'], iTotalRecords=(total_data), iTotalDisplayRecords=total_data,
                                        aaData=user_data)
        except Exception as exc:
            print(exc.message)

    elif request.method == 'POST' and request.POST.get('modal_use',''):
        search_param = {"id":int(request.POST.get("user_id",0))}
        main_data = CreateUser.objects.filter(**search_param)
        user_data = {}
        for values in main_data:
                #,

                user_data = {"user_name":values.user_name,"email_id":values.email_id,"mobile_number":values.mobile_number,
                                 "credit_available":str(values.credit_available) if values.credit_available else 0,"credit_used":str(values.credit_used)
                    if values.credit_used else 0,"address":values.address,
                                 "credit_assigned":str(values.credit_assigned),"user_role":values.user_role,"user_id":values.id
                                  }
                response = user_data


    return HttpResponse(json.dumps(response))





@csrf_exempt
def edit_user_details(request):
    try:
        user_id = None
        if request.is_ajax():
            user_id = request.POST.get('user_id', None)

            validate_edit_form = user_form.CreateUserForms(request.POST,user_role=request.session['role'])
            # if validate_edit_form.is_valid():
            user_name = request.POST.get('user_name', None)
            email_id = request.POST.get('email_id', None)
            address = request.POST.get('address', None)
            credit_assigned = request.POST.get('credit_assigned', None)
            credit_available = request.POST.get('credit_available', None)
            credit_used = request.POST.get('credit_used', None)
            credit_result = get_user_credits(request.session['parent_id'])
            parent_user_credit_used = credit_result['credit_used']
            parent_user_credit_available = credit_result['credit_available']
            credit = request.POST.get('credit', None)
            if float(credit) > float(parent_user_credit_available):
                message = "Don't have enough credits."
                res = dict(status='true', msg="Don't have enough credits.")
                return HttpResponse(json.dumps(res))

            mobile_number = request.POST.get('mobile_number', None)
            search_param = {"id":int(request.POST.get("user_id",0))}
            CreateUser.objects.filter(**search_param).update(user_name=user_name,email_id=email_id,
                                   mobile_number=mobile_number,
                                   credit_assigned=float(credit_assigned)+float(credit),
                                   credit_available=float(credit_available)+float(credit),
                                   credit_used=credit_used,
                                   address=address)
            search_param = {"id": int(request.session['parent_id'])}
            CreateUser.objects.filter(**search_param).update(
                credit_available=float(parent_user_credit_available) - float(credit),
                credit_used=float(parent_user_credit_used) + float(credit),
            )

            res = dict(status='true', msg='User details has been successfully updated')
            return HttpResponse(json.dumps(res))
            # else:
            #     error = validate_edit_form._errors
            #     print error
            #     error['status'] = 'false'
            #     error['msg'] = 'Please ensure data to be submitted is valid'
            #     # response = dict(status='false', msg='Please ensure data to be submitted is valid')
            #     return HttpResponse(json.dumps(error))


    except Exception as ex:
        print ex.message
        raise Http404
