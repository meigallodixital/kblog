from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from .models import Post

User = get_user_model()

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f'title {n}')
    body = factory.Sequence(lambda o: f'body {o}')
    author = factory.Iterator(User.objects.all())

