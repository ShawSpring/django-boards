from django.test import TestCase
from django.urls import resolve
from django.core.urlresolvers import  reverse
from ..views import topic_posts,PostListView
from ..models import Topic,Board,Post
# from django.contrib.auth.models import User
from django.contrib.auth import  get_user_model
User = get_user_model()


class TopicPostsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name='Django', description='Discussion about Django.')
        self.user = User.objects.create_user(
            username='xcl', email='xiaochunlai@163.com', password='123')
        topic = Topic.objects.create(subject='Hello,Django',starter = self.user,board=self.board)
        post = Post.objects.create(message='just say hello to Djano',created_by=self.user,topic=topic)
        url = reverse('topic_posts',kwargs={'pk':topic.board.pk,'topic_pk':topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_url_resolves_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEqual(view.func.view_class,PostListView)
