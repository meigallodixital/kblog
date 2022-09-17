from django.db import transaction
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from account.factories import UserFactory  


class Command(BaseCommand):
    help = "Generates users test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Start creating new users data...")
        try:
            for _ in range(20):
                UserFactory()
        except IntegrityError:
            self.stdout.write("This command was runned before\nClean the auth_user table on database if you want to run it again")
        else:
            self.stdout.write("End creating new users data...")