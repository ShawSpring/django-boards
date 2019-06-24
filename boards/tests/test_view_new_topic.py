from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from ..views import home, board_topics, new_topic
from django.shortcuts import resolve_url
from ..models import Board, Topic, Post, User
from ..forms import NewTopicForm


class NewTopicTest(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
            name='Django', description='Discussion about Django.')
        self.user = User.objects.create_user(
            username='xcl', email='xiaochunlai@163.com', password='123')
        self.client.login(username='xcl',password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject':
                'Test Title',
            'message':
                'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """
        invalid data shoud not  redirect
        the excepted behavior  is to show the form again with validation error
        redirect 的状态码是 302， 而如果直接返回一个页面的话 是 200
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        不应 redirect,而应再次显示 表单 ,而且也不应该创建 Topic 和 Post实例
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {'subject': '', 'message': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid	post	data	should	not	redirect
        The	expected	behavior	is	to	show	the	form	again	with	
        validation	errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name='Django', description='Discussion about Django.')
        self.url=reverse('new_topic',kwargs={'pk':1})
        self.response = self.client.get(self.url)
    def test_redirection(self):
        """
         没有登录的情况下 访问 new_topic 结果是重定向
        """
        login_url = reverse('login')
        self.assertRedirects(self.response,f"{login_url}?next={self.url}")

