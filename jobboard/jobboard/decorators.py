from django.shortcuts import redirect, reverse
from django.contrib import messages

# Define the login_required decorator
def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        request.session["next_path"] = request.path
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page.")
            return redirect(f"{reverse('app1:login_page')}?next={request.session['next_path']}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
