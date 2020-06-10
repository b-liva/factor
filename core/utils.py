from graphql_jwt.decorators import login_required


class OwnQuerySet:
    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        user = info.context.user
        queryset = queryset.filter(is_active=True)
        if not user.is_superuser:
            return queryset.filter(owner=user)
        return queryset
