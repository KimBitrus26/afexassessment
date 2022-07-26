from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse


def login_required_with_feedback(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('login'))

    return wrapper


# def user_is_business_owner(func):
   
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         business_slug = kwargs.get("business_slug")

#         if business_slug:
#             business = get_object_or_404(Business, slug=business_slug)
#         else:
#             return func(request, *args, **kwargs)

#         if business.user == request.user:
#             return func(request, *args, **kwargs)
#         else:
#             messages.info(request, "You must be business owner to access a business")
#             return HttpResponseRedirect(reverse('manage'))

#     return wrapper


