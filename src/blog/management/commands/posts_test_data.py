from django.db import transaction
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from blog.factories import PostFactory  


class Command(BaseCommand):
    help = "Generates posts test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Start creating new posts data...")
        try:
            for _ in range(200):
                PostFactory()
        except IntegrityError:
            self.stdout.write("This command was runned before\nClean the blog_post table on database if you want to run it again")
        else:
            self.stdout.write("End creating new posts data...")