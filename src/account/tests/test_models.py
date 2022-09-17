import copy
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class UsersModelsTestCase(TestCase):
    """ Model Users tests """

    def setUp(self):
        self.user_data = {
            'first_name': 'user',
            'last_name': 'subname',
            'email': 'user@kblog.com',
            'username': 'user',
            'password': 'samepasswordforall2022'
        }

        self.user1 = User.objects.create_user(**self.user_data)

    def test_str_user(self):
        """ Test if str return username """
        self.assertEqual(str(self.user1), self.user1.username)

    def test_same_username(self):
        """ Test if  username duplicates are checked """
        data = copy.copy(self.user_data)
        data['email'] = "false@kblog.com"

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**data)

        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(email='false@kblog.com')

    def test_same_email(self):
        """ Test if  email duplicates are checked """
        data = copy.copy(self.user_data)
        data['username'] = "user2"

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**data)

        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='user2')

    def test_modify_user(self):
        """ Test User modify """
        self.user1.first_name = 'changed'
        self.user1.save()
        self.assertEqual(self.user1.first_name, 'changed')

    def test_delete_user(self):
        """ Test User delete """
        data = copy.copy(self.user_data)
        data['username'] = 'test'
        data['email'] = 'test@test'

        # Create new user
        user2 = User.objects.create_user(**data)
        self.assertNotEqual(user2, None)

        # Check user exists
        user2 = User.objects.get(username='test')
        self.assertNotEqual(user2, None)

        # Delete new user
        user2.delete()
        with self.assertRaises(ObjectDoesNotExist):
            user2 = User.objects.get(username='test')

    def tearDown(self):
        self.user1.delete()
