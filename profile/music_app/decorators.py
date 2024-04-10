from django.http import HttpResponse
from django.shortcuts import redirect

# def login_required(login_url=''):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return login_url(request, *args, **kwargs)
#         else:
#             return redirect('login')
#     return wrapper_func

# create a decorator for pass in list of roles
def allowed_users(allowed_roles=['admin_role',]):
    # create decorator and pass in view function
    # decorator is placed above the view function
    def decorator(view_func):
        # create wrapper function to check if user is in allowed_roles
        def wrapper_func(request, *args, **kwargs):
            # debug and print allowed roles
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

def user_is_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        artist = request.artist
        if request.user == args[0].artist:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func