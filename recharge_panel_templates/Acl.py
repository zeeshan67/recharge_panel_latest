import logging

from django.http import Http404, HttpResponseRedirect

# from aawaz_panel.models import permissions_model, roles_model

class Acl:
    def __init__(self):
        pass

    def process_request(self, request):
        try:
            role = request.session.get('role', "guest")
            request_path = request.path
            print role
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = None
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            # if str(path_id['_id']) in role_permissions['permissions']:
            #     request.session['current_url'] = request_path
            #     return None
            if role in ("admin","retailer","distributor") or request_path  in ('/login/','/'):
                return None
            # elif role == "user":
            #     return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
        except TypeError as e:
            print "Error in ACL %s"%e.message
        raise Http404