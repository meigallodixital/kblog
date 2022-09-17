from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory


User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)
    email =  factory.LazyAttribute(lambda o: '%s@kblog.org' % o.username)
    password = factory.PostGenerationMethodCall('set_password', 'testusers2022')
