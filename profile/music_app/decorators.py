from django.http import HttpResponse
from django.shortcuts import redirect

# def login_required(login_url=''):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return login_url(request, *args, **kwargs)
#         else:
#             return redirect('login')
#     return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('role', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

