from django.contrib.auth.models import Permission


def grant_django_model_permissions(user, perms):
    for perm in perms:
        user.user_permissions.add(
            Permission.objects.get(codename=perm[0], content_type__app_label=perm[1])
        )
    return user
