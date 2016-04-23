from django.template import RequestContext, loader
from django.http import HttpResponse
from recharge_panel_app.forms import user_form
from recharge_panel_app.models import CreateUser
import hashlib


def add_user(request):
    message = ''
    new_user_form = user_form.CreateUserForms()
    context_data = RequestContext(request,
                                  {'body_template': 'user/create_user.html',
                                   'session_data': request.session,
                                   "success": "false",
                                   "error": "error"})
    try:
        context_data['form'] = new_user_form
        if request.method == "POST":
            print request.POST, 'posttttttttttttttttttt'
            new_user_form = user_form.CreateUserForms(request.POST)
            user_name = request.POST['user_name']
            email_id = request.POST['email_id']
            mobile_number = request.POST['mobile_number']
            password = hashlib.md5(request.POST['password'])
            address = request.POST['address'] if request.POST['address'] else ''
            user_data = CreateUser(user_name=user_name,
                                   email_id=email_id,
                                   mobile_number=mobile_number,
                                   password=password,
                                   address=address)
            user_data.save()
    except Exception as e:
        print "Exception %s" % e.message
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))
