import graphene
from graphene_django.types import DjangoObjectType
from .models import Perm, PermSpec


class PermType(DjangoObjectType):
    class Meta:
        model = Perm


class PermSpecType(DjangoObjectType):
    class Meta:
        model = PermSpec


class Query(object):
    perm = graphene.Field(PermType,
                          id=graphene.Int(),
                          number=graphene.Int())

    all_perms = graphene.List(PermType,
                              number=graphene.Int())

    perm_spec = graphene.Field(PermSpecType,
                               id=graphene.Int(),
                               )
    all_perm_specs = graphene.List(PermSpecType)

    def resolve_perm(self, info, **kwargs):
        id = kwargs.get('id')
        number = kwargs.get('number')

        if id is not None:
            return Perm.objects.get(id=id)
        if number is not None:
            return Perm.objects.get(number=number)
        return None

    def resolve_all_perms(self, info, **kwargs):
        number = kwargs.get('number')
        if number is not None:
            return Perm.objects.filter(number=number)
        return Perm.objects.all()

    def resolve_perm_spec(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return PermSpec.objects.get(id=id)
        return None

    def resolve_all_perm_specs(self, info, **kwargs):
        return PermSpec.objects.all()
