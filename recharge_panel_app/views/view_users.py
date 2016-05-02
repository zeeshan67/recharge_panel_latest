from django.template import RequestContext, loader
from django.http import HttpResponse
from recharge_panel_app.forms import user_form
from recharge_panel_app.models import CreateUser
import hashlib


def view_user(request):
    role = request.session['role']
    context_data = RequestContext(request,
                                  {'body_template': 'user/view_user.html',
                                   'session_data': request.session,
                                   "success": "false",
                                   "error": "error"})
    template = loader.get_template('commons/index.html')
    return HttpResponse(template.render(context_data))
