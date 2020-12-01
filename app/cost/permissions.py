from rest_framework import permissions


class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.read_%(model_name)s']


class CustomDjangoObjectPermissions(permissions.DjangoObjectPermissions):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
