from request.models import Requests
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin


class OwnRequestMixin(MultipleObjectMixin):
    """
    Only returns objects that belongs to the current user. Assumes the object
    has a 'user' foreignkey to a User.
    """

# class CustomerRequestOwnerMixin(SingleObjectMixin):
#     pass