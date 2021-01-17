import faker

from django.contrib.auth import get_user_model
from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory


fake = faker.Faker()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    password = PostGenerationMethodCall('set_password', fake.password(length=42, special_chars=True, digits=True, upper_case=True, lower_case=True))
    # password = PostGenerationMethodCall('set_password', 'My_Password_555')

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
