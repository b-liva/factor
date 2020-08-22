from django.db.models import Q

from core.models import UserRelation
from request.models import Xpref, Requests, ReqSpec


class AccessControl:
    def __init__(self, user, permission=None, obj=None):
        self.obj = obj
        self.user = user
        self.permission = permission

    def allow(self):
        pass

    def show(self):
        pass

    def get_related_users(self):
        users_list = []
        parents = UserRelation.objects.filter(child=self.user)
        children = UserRelation.objects.filter(parent=self.user)
        if parents.exists():
            users_list.extend([user.parent for user in parents])

        if children.exists():
            children = children[0].child.all()
            users_list.extend([user for user in children])

        users_list.extend([self.user])
        return users_list


class OrderProxy(AccessControl):
    model = Requests
    lookup = 'request_pk'

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        users_list = self.get_related_users()
        if self.obj.owner in users_list or len(set(users_list).intersection(set(self.obj.colleagues.all()))) > 0:
            return self.user.has_perm(self.permission)

        return False

    def show(self):
        if self.user.is_superuser:
            return Q()
        users_list = self.get_related_users()
        print('user; ', users_list)
        return Q(owner__in=users_list) | Q(colleagues__in=users_list)


class SpecProxy(AccessControl):
    model = ReqSpec
    lookup = 'yreqSpec_pk'

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        users_list = self.get_related_users()
        if self.obj.req_id.owner in users_list or len(set(users_list).intersection(set(self.obj.req_id.colleagues.all()))) > 0:
            return self.user.has_perm(self.permission)

        return False

    def show(self):
        if self.user.is_superuser:
            return Q()
        users_list = self.get_related_users()
        print('user; ', users_list)
        return Q(owner__in=users_list) | Q(colleagues__in=users_list)


class ProformaProxy(AccessControl):
    model = Xpref
    lookup = 'ypref_pk'

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


class PaymentProxy(AccessControl):

    def allow(self):
        if self.user.is_superuser:
            return True
        if not self.obj:
            return self.user.has_perm(self.permission)
        if self.obj.owner == self.user or self.user == self.obj.xpref_id.owner or self.user == self.obj.xpref_id.req_id.owner or self.user in self.obj.xpref_id.req_id.colleagues.all():
            return self.user.has_perm(self.permission)

        return False

