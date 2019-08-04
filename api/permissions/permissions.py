from rest_framework import permissions
from django.shortcuts import get_object_or_404
from request.models import ReqSpec, Requests


class IsSuperUserOrOwner(permissions.DjangoModelPermissions):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        # if request.method == 'DELETE' or request.method == 'PUT' or :
        perm = super().has_permission(request, view)
        print('perm: ', perm)
        if 'pk' in view.kwargs:
            obj = get_object_or_404(Requests, pk=view.kwargs['pk'])
            return request.user == obj.owner or request.user.is_superuser
        return perm

