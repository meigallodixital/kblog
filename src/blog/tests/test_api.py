import copy
import datetime

from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post


class PostsAPITestCase(APITestCase):
    """ API Post tests """

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

        self.post1 = {'title': 'one one',
                      'body': 'one one', 'published_at': now()}
        self.post2 = {'title': 'two two',
                      'body': 'two two', 'published_at': now()}

        self.token1 = None
        self.refresh1 = None
        self.token2 = None
        self.refresh2 = None

        self.url_register = reverse('user:create_user')
        self.verification_url = reverse('token_verify')
        self.login_url = reverse('token_obtain_pair')
        self.create_post_url = reverse('blog:post-create')
        self.list_post_url = reverse('blog:post-list')

        self.__create_users()
        self.__get_tokens()
        self.__create_posts()

    def __create_users(self):
        """ Persistent users """
        response = self.client.post(self.url_register, self.user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url_register, self.user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def __get_tokens(self):
        """ Persistent tokens """
        response = self.client.post(self.login_url, {
                                    'username': self.user1['username'], 'password': self.user1['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.
                        data)
        self.token1 = response.data['access']
        self.refresh1 = response.data['refresh']

        response = self.client.post(self.login_url, {
                                    'username': self.user2['username'], 'password': self.user2['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.token2 = response.data['access']
        self.refresh2 = response.data['refresh']

    def __create_posts(self):
        """ Persistent posts """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.post(self.create_post_url, self.post1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], 'one-one')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.post(self.create_post_url, self.post2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], 'two-two')

    def test_bad_post_create(self):
        """ Create post  without auth or with bad data """
        # Anonymous tries create post without authorization
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ABC')
        response = self.client.post(
            self.create_post_url, self.post1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Auth create post with bad data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.post(self.create_post_url, {'test': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_list(self):
        """ List posts """
        response = self.client.get(self.list_post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), response.data.get('count'))

    def test_post_view(self):
        """ View posts """
        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post1['title'])})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], slugify(self.post1['title']))

        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post2['title'])})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], slugify(self.post2['title']))

    def test_post_edit(self):
        """Edit post with put and patch"""
        data = {
            "title": "changed",
            "body": "body changed"
        }

        # Edit post with owner
        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post1['title'])})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['body'], data['body'])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.patch(url, {'title': data['title'] + '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'] + '2')

        # Try to edit user2 post with user 1
        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post2['title'])})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.patch(url, {'title': data['title'] + '2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete(self):
        """ Delete post """
        # Delete user2 post
        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post2['title'])})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete user1 post with user2
        url = reverse('blog:post-view-update-delete',
                      kwargs={'slug': slugify(self.post1['title'])})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_published_in_future(self):
        """ In future Post """
        post = copy.copy(self.post1)
        post['title'] = "future"
        post['published_at'] = datetime.datetime.now() + \
            datetime.timedelta(days=1)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        response = self.client.post(self.create_post_url, post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # As we have one on future reponse count must be database count - 1
        response = self.client.get(self.list_post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count()-1, response.data.get('count'))
