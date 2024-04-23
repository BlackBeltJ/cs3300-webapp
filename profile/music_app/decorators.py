from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Artist

# create a decorator for pass in list of roles
def allowed_users(allowed_roles=['admin_role','artist_role']):
    # create decorator and pass in view function
    # decorator is placed above the view function
    def decorator(view_func):
        # create wrapper function to check if user is in allowed_roles
        def wrapper_func(request, *args, **kwargs):
            # debug and print allowed roles
            print('role', allowed_roles)
            group = None
            # check if user is in a group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            # check if user is in allowed_roles
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You do not have permission to perform that action ')
                return redirect('index')
        return wrapper_func
    return decorator

def user_is_owner():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('args', args) # displays args and kwargs for debugging purposes
            print('kwargs', kwargs)
            # grab the current user from 'request'
            user = request.user
            # use the kwarg pk from the view_func to get the artist object
            artist = Artist.objects.get(id=kwargs['pk'])
            # check if the user is associated to the artist
            if user == artist.user:
                # if the logged in user it the owner of the artist, call the view_func
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You do not have permission to perform that action ')
                return redirect('index')
        return wrapper_func
    return decorator
