from django.contrib.auth.models import Group
from faker import Factory
import factory
from django.contrib.auth import get_user_model
User = get_user_model()

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = faker.user_name()
    first_name = faker.user_name()
    last_name = faker.user_name()
    password = factory.PostGenerationMethodCall('set_password', faker.password())


def create_user(**kwargs):
    user = UserFactory.create(**kwargs)
    return user


def add_user_to_groupe(user, group='sale_expert'):
    sale_expert_group = Group.objects.get(name=group)
    user.groups.add(sale_expert_group)
    return user
