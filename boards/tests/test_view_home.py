from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from ..views import home, board_topics, new_topic,BoardListView
from django.shortcuts import resolve_url
from ..models import Board, Topic, Post, User
from ..forms import NewTopicForm

class HomeTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(
            name='django', description='Django discussion board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response,
                            'href="{0}"'.format(board_topics_url))
