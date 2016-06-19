import logging

from django.http import Http404, HttpResponseRedirect,HttpResponse
import fnmatch,json

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

            print(request_path)
            filter_cond = []
            filter_cond.append(request_path)
            if fnmatch.filter(filter_cond, '/mobile_apps*'):
                print("Got request from Mobile App")
                auth_key = (request.META.get('HTTP_AUTHORIZATION',None))
                if auth_key:
                    token = auth_key.split(' ')[1]
                    if token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJoYXBweXBvY2tldEAxMjMiLCJpYXQiOjE0NjYwNzM4MjksImV4cCI6MTQ2NjY3MzgyOX0.kzCBftKdjk1MjQtIZR5GYdSxP2bxFgdBImrKxbAJmFo":
                        print("token matches")
                        return None
                    else:
                        return HttpResponse(json.dumps({"code":401,"msg":"Unauthorized access not allowed"}), status=401)
                return HttpResponseRedirect('/login')

            if role in ("admin","retailer","distributor") or request_path  in ('/login/','/'):
                return None
            # elif role == "user":
            #     return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
        except TypeError as e:
            print "Error in ACL %s"%e.message
        raise Http404