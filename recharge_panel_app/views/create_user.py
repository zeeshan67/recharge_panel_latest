from django.template import RequestContext, loader
from django.http import HttpResponse
from recharge_panel_app.forms import user_form
from recharge_panel_app.models import CreateUser,get_user_credits
import hashlib


def add_user(request):
    message = ''
    role = request.session['role']
    new_user_form = user_form.CreateUserForms(user_role=role)
    user_id = request.session['user_id']
    context_data = RequestContext(request,
                                  {'body_template': 'user/create_user.html',
                                   'session_data': request.session,
                                   "success": "false",
                                   "error": "error"})
    try:
        context_data['form'] = new_user_form
        if request.method == "POST":
            new_user_form = user_form.CreateUserForms(request.POST,user_role=role)
            if new_user_form.is_valid():
                user_name = request.POST['user_name']
                email_id = request.POST['email_id']
                mobile_number = request.POST['mobile_number']
                password = hashlib.md5(request.POST['password']).hexdigest()
                credit_assigned = request.POST['credit_assigned']
                credit_used = request.POST['credit_used']
                credit_available = request.POST['credit_available']
                address = request.POST['address'] if request.POST['address'] else ''
                credit_result = get_user_credits(request.session['parent_id'])
                parent_user_credit_used = credit_result['credit_used']
                parent_user_credit_available = credit_result['credit_available']
                print "CREDITS %s - %s"%(credit_available,parent_user_credit_available)
                if float(credit_available) > float(parent_user_credit_available):
                    context_data['error'] = "true"
                    message = "Don't have enough credits."
                    context_data['form'] = new_user_form
                else:
                    user_data = CreateUser(user_name=user_name,
                                           email_id=email_id,
                                           credit =credit_assigned,
                                           mobile_number=mobile_number,
                                           password=password,
                                           parent_id= int(request.session['user_id']),
                                           user_role = request.POST['user_role'],
                                           credit_assigned=credit_assigned,
                                           credit_available=credit_available,
                                           credit_used=credit_used,
                                           address=address)
                    user_data.save()
                    search_param = {"id": int(request.session['parent_id'])}
                    CreateUser.objects.filter(**search_param).update(
                                                                     credit_available=float(parent_user_credit_available)-float(credit_available),
                                                                     credit_used=float(parent_user_credit_used)+float(credit_used),
                                                                     )

                    context_data['success'] = "true"
                    message = "User created successfully."
            else:
                context_data['error'] = "true"
                message = "Error while creating user."
                context_data['form'] = new_user_form
            context_data['message'] = message
    except Exception as e:
        print "Exception %s" % e.message
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))
