from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from ..views import PostUpdateView
from ..models import Post, Topic, Board, User



class PostUpdateViewTestCase(TestCase):

    def setUp(self):
        self.username = 'xcl'
        self.password = '123'
        self.user = User.objects.create_user(
            username=self.username,
            email='xiaochunlai@163.com',
            password=self.password)
        self.board = Board.objects.create(
            name='Django', description='Discussion about Django.')
        self.topic = Topic.objects.create(
            subject='Hello,Django', board=self.board, starter=self.user)
        self.post = Post.objects.create(
            message='this is a message', created_by=self.user, topic=self.topic)
        self.url = reverse(
            'post_edit',
            kwargs={
                'pk': self.board.pk,
                'topic_pk': self.topic.pk,
                'post_pk': self.post.pk
            })

class LoginRequiredPostUpdateViewTest(PostUpdateViewTestCase):
    def test_Redirection(self):
        login_url = reverse('login')
        response= self.client.get(self.url)

        self.assertRedirects(response,f'{login_url}?next={self.url}')

class UnauthorizedPostUpdateViewTest(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'xxxx'
        password = '123'
        user = User.objects.create_user(
            username=username,
            email='xxxx@163.com',
            password=password)
        self.client.login(username = username,password=password)
        self.response = self.client.get(self.url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code,404)
