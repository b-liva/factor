import graphene
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id


class OwnQuerySet:
    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        user = info.context.user
        queryset = queryset.filter(is_active=True)
        if not user.is_superuser:
            return queryset.filter(owner=user)
        return queryset


class DeletePermissionCheck:

    msg = graphene.String()
    number = graphene.Int()

    @classmethod
    def mutate(cls, root, info, input):
        number = None
        try:
            obj = input.model._default_manager.get(
                pk=from_global_id(input.id)[1]
            )
            obj.delete()
            if hasattr(obj, 'number'):
                number = obj.number
                msg = f"{input.label} شماره {obj.number} با موفقیت حذف گردید."
            else:
                msg = "با موفقیت حذف شد."
        except:
            msg = f"بروز خطا"
        return cls(
                msg=msg,
                number=number
            )

