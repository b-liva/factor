from django.db.models import Q


class AccessControl:
    def __init__(self, access_obj):
        self.access_obj = access_obj

    def allow(self):
        return self.access_obj.allow()

    def show(self):
        return self.access_obj.show()


class OrderProxy:
    def __init__(self, user, permission, obj=None):
        self.obj = obj
        self.user = user
        self.permission = permission

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        if self.user == self.obj.owner or self.user in self.obj.colleagues.all():
            return self.user.has_perm(self.permission)

        return False

    def show(self):
        if self.user.is_superuser:
            return Q()
        return Q(owner=self.user) | Q(colleagues=self.user)


class ProformaProxy:
    def __init__(self, user, permission, obj=None):
        self.obj = obj
        self.user = user
        self.permission = permission

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        if self.user == self.obj.owner or self.user == self.obj.req_id.owner or self.user in self.obj.req_id.colleagues.all():

            return self.user.has_perm(self.permission)

        return False


class PaymentProxy:
    def __init__(self, user, permission, obj=None):
        self.obj = obj
        self.user = user
        self.permission = permission

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        if self.obj.owner == self.user or self.user == self.obj.xpref_id.owner or self.user == self.obj.xpref_id.req_id.owner or self.user in self.obj.xpref_id.req_id.colleagues.all():
            return self.user.has_perm(self.permission)

        return False

