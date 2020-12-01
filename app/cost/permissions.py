from rest_framework import permissions


class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.read_%(model_name)s']
