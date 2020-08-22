from django.db.models import Q

from core.models import UserRelation


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

    def get_related_users(self):
        users_list = []
        parents = UserRelation.objects.filter(child=self.user)
        childs = UserRelation.objects.filter(parent=self.user)
        if parents.exists():
            users_list.extend([user.parent for user in parents])

        if childs.exists():
            childs = childs[0].child.all()
            users_list.extend([user for user in childs])

        users_list.extend([self.user])
        return users_list

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)

        users_list = self.get_related_users()
        if self.obj.owner in users_list or self.obj.req_id.owner in users_list or \
                len(set(users_list).intersection(set(self.obj.req_id.colleagues.all()))) > 0:
            return self.user.has_perm(self.permission)

        return False

    def show(self):
        if self.user.is_superuser:
            return Q()

        users_list = self.get_related_users()

        return Q(owner__in=users_list) | Q(req_id__colleagues__in=users_list) | Q(req_id__owner__in=users_list)


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

