import copy
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from blog.models import Post


User = get_user_model()


class PostsModelsTestCase(TestCase):
    """ Model Users tests """

    def setUp(self):

        self.user_data = {
            'first_name': 'user',
            'last_name': 'subname',
            'email': 'user@kblog.com',
            'username': 'user',
            'password': 'samepasswordforall2022',
        }
                
        self.user1 = User.objects.create_user(**self.user_data)
        
        self.post_data = {
            'title': 'post1',
            'body': 'body1',
            'published_at': now(),
            'author': self.user1
        }


    def test_str_post(self):
        """ Test if str return title """
        self.assertEqual(str(self.user1), self.user1.username)

    def test_create_post(self):
        """ Test create post """
        post = Post.objects.create(**self.post_data)
        self.assertNotEqual(post, None)
        self.assertEqual(post.title, self.post_data['title'])
        self.assertEqual(post.body, self.post_data['body'])
        self.assertEqual(post.author, self.user1)
    
    def test_duplicate_post(self):
        self.post = Post.objects.create(**self.post_data)
        with self.assertRaises(IntegrityError):
            self.post = Post.objects.create(**self.post_data)

    def test_modify_post(self):
        """ Test modify post """
        Post.objects.create(**self.post_data)
        post = Post.objects.get(title=self.post_data['title'])
        post.title = 'changed'
        post.save()

        post_test = Post.objects.get(pk=post.id)
        self.assertEqual(post_test.title, 'changed')

    def test_delete_post(self):
        """ Test delete post """
        Post.objects.create(**self.post_data)
        post = Post.objects.get(title=self.post_data['title'])
        post.delete()

        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(title=self.post_data['title'])

    def tearDown(self):
        self.user1.delete()
