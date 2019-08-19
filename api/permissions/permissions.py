from rest_framework import permissions
from django.shortcuts import get_object_or_404

from request.models import ReqSpec, Xpref


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map.update({'GET': ['%(app_label)s.index_%(model_name)s']})
        # self.perms_map.update({'GET': []})


class IsSuperUserOrOwner(permissions.DjangoModelPermissions):

    def get_required_permissions(self, method, model_cls):
        perms = super().get_required_permissions(method, model_cls)
        # print(perms, method, model_cls._meta)
        # if method == 'GET' and model_cls == ReqSpec:
            # print(perms, method, model_cls._meta)
            # print(self.perms_map['GET'], model_cls)
            # todo: why 'request.index_reqspec' that dosen't exist is required? this class extends DjangoModelPermissions?
            # two ways to handle: 1- add the line bellow 2- add index_reqspec to the ReqSpec model permissions.
            # self.perms_map['GET'] = []
        return perms

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        # if request.method == 'DELETE' or request.method == 'PUT' or :
        perm = super().has_permission(request, view)
        mdl = self._queryset(view).model
        if 'pk' in view.kwargs:
            obj = get_object_or_404(mdl, pk=view.kwargs['pk'])
            return request.user == obj.owner or request.user.is_superuser
        if 'number' in view.kwargs:
            obj = get_object_or_404(mdl, number=view.kwargs['number'])
            return request.user == obj.owner or request.user.is_superuser
        return perm

    # def get_required_permissions(self, method, model_cls):
    #     output = super().get_required_permissions(method, model_cls)
    #     print('method: ', method)
    #     print('model_cls: ', model_cls)
    #     self.model_name = model_cls
    #     print(output)
    #     return output

