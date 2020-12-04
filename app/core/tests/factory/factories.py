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
