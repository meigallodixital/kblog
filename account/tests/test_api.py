import copy

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APIUsersTestCase(APITestCase):
    """ API Users tests """

    def setUp(self):
        self.user1 = {
            'username': 'test_user_1',
            'first_name': 'test',
            'last_name': 'user 1',
            'email': 'test_user_1@test.com',
            'password': 'samepasswordforall2022',
            'password2': 'samepasswordforall2022',
        }
        self.user2 = {
            'username': 'test_user_2',
            'first_name': 'test',
            'last_name': 'user 2',
            'email': 'test_user_2@test.com',
            'password': 'samepasswordforall2022',
            'password2': 'samepasswordforall2022',
        }

        self.token1 = None
        self.refresh1 = None
        self.token2 = None
        self.refresh2 = None

        self.url_register = reverse('user:create_user')
        self.verification_url = reverse('token_verify')
        self.login_url = reverse('token_obtain_pair')
        self.get_info_url = reverse('user:user_info')

        self.__create_users()
        self.__get_tokens()

    def __create_users(self):
        """ Create two users """
        response = self.client.post(self.url_register, self.user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url_register, self.user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def __get_tokens(self):
        """ Gets tokens """
        response = self.client.post(self.login_url, {
                                    'username': self.user1['username'], 'password': self.user1['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.token1 = response.data['access']
        self.refresh1 = response.data['refresh']

        response = self.client.post(self.login_url, {
                                    'username': self.user2['username'], 'password': self.user2['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.token2 = response.data['access']
        self.refresh2 = response.data['refresh']

    def test_duplicate_email(self):
        """ Check duplicated email """
        user = copy.copy(self.user1)
        user['username'] = 'distinct username to test email duplicated'
        response = self.client.post(self.url_register, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        """ Check duplicated username """
        user = copy.copy(self.user1)
        user['email'] = 'distinctemail@totestusernameduplicated.com'
        response = self.client.post(self.url_register, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_tokens(self):
        """ Check tokens """
        response = self.client.post(
            self.verification_url, {'token': self.token1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.verification_url, {'token': self.token2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check bad token
        response = self.client.post(self.verification_url, {'token': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accesses(self):
        """ Check accesses """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.get(self.get_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.get(self.get_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        response = self.client.get(self.get_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
