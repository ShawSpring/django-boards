from django.test import TestCase
from django.urls import resolve
from django.core.urlresolvers import reverse
from ..models import Topic,Board,Post,User
from ..views import topic_reply
from ..forms import PostForm

class TopicReplyTestCase(TestCase):
    def setUp(self):
        self.username ='xcl'
        self.password  = '123'
        self.board = Board.objects.create(
            name='Django', description='Discussion about Django.')
        self.user = User.objects.create_user(
            username=self.username, email='xiaochunlai@163.com', password=self.password)
        self.topic = Topic.objects.create(subject = 'Hello,Django',
            board=self.board,starter=self.user)  
        self.post = Post.objects.create(message='this is a message',created_by = self.user,
            topic = self.topic)
        self.url = reverse('topic_reply',kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})
        
class LoginRequiredTests(TopicReplyTestCase):
    def test_redirection(self):
        response =self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response,f'{login_url}?next={self.url}')

class TopicReplyTests(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username = self.username,password = self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_csrf(self):
        self.assertContains(self.response,'name=\'csrfmiddlewaretoken')

    def test_url_resolves_view_function(self):
        view = resolve(self.url)
        self.assertEqual(view.func,topic_reply)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PostForm)
    
    def test_contains_inputs(self):
        self.assertContains(self.response,'<input ',1)
        self.assertContains(self.response,'<textarea ',1)

class SuccessfulTopicReplyTest(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username,password = self.password)
        self.response = self.client.post(self.url,{'message':'this is a message'})
    
    def test_redirection(self):
        topic_posts_url = reverse('topic_posts',kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})
        self.assertRedirects(self.response,topic_posts_url)
    
    def test_reply_created(self):
        self.assertEqual(Post.objects.count(),2)


class InvalidTopicReply(TopicReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username,password=self.password)
        self.response = self.client.post(self.url,{})
    
    def test_reply_didnt_created(self):
        self.assertEqual(Post.objects.count(),1)
    
    def test_form_error(self):
        form =self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_status_code(self):
        """
        post失败，返回原页面
        """
        self.assertEqual(self.response.status_code,200)
