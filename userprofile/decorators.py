# decorators.py
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps

def paid_account_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.account_type == 'paid':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('upgrade_account')  # Redirect to the upgrade account page
    return _wrapped_view
