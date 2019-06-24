from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.http import HttpResponse, Http404
# Create your views here.
from .models import Board, Topic, Post, User
from django.contrib.auth.decorators import login_required
from .forms import NewTopicForm, PostForm
from django.views.generic import UpdateView, ListView
from django.db.models import Count
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# 视图函数 都是 接收 HttpRequest 并返回 HttpResponse
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


## 使用 CBV 重构 home
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'  ### listview 应该自动将 boards => 一系列的 Board model
    template_name = 'home.html'


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(
        replies=Count('posts') - 1)
    paginator = Paginator(queryset, 20)  ##一页二十条记录

    page = request.GET.get(
        'page', 1)  ## 默认为1 HttpRequest.GET 是个 dictionary-like object,
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)  #最后一页
    # topics 以前是一个 查询集， 使用了paginator后，是一个paginator.page对象， 都是一个 Iterator
    return render(request, 'topics.html', {'board': board, 'topics': topics})


"""
和 上面 board_topics 一样的功能，一个是FBV 一个是cbv
"""


class TopicListView(ListView):
    model = Topic
    template_name = 'topics.html'
    context_object_name = 'topics'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(
            replies=Count('posts') - 1)

        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(
                commit=False)  # 返回一个Topic（）,因为 form的mate中，定义了 model = Topic
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user)

            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()  # 如果请求是GET 初始化一个空表单
    return render(request, 'new_topic.html', {'board': board, 'form': form})

    # subject = request.POST['subject']
    # message = request.POST['message']
    # topic = Topic.objects.create(subject=subject,board=board,starter=user)
    # post = Post.objects.create(message=message,topic=topic,created_by=user)
    # return redirect('board_topics',pk=pk)


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, id=topic_pk, board_id=pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


"""
topic_posts的 cbv实现
"""


class PostListView(ListView):
    model= Post
    context_object_name	= 'posts'
    template_name = 'topic_posts.html'
    paginate_by	=	5

    def get_context_data(self, **kwargs):
        session_key = f'viewd_topic_{self.topic.id}'

        """
        第一次浏览 这个topic后 设置为True 以后在看时因为 session[session_key]==True，就不会在计算views
        """
        if not self.request.session.get(session_key,False): 
            self.topic.views +=1
            self.topic.save()
            self.request.session[session_key] = True
        
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, 
            id=self.kwargs.get('topic_pk'),board_id=self.kwargs.get('pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset ##queryset 经过分页后 变成 object_list 即 posts


@login_required
def topic_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, id=topic_pk, board_id=pk)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.topic = topic
            post.last_updated = timezone.now()
            post.save()

            topic_url = reverse('topic_posts',kwargs={'pk':pk,'topic_pk':topic_pk})
            # url = f"{topic_url}?page={topic.get_page_count()}#{post.id}"
            url = f"{topic_url}?page={1}#{post.id}"
            
            return redirect(url)
    else:
        form = PostForm()
    return render(request, 'topic_reply.html', {'topic': topic, 'form': form})



@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = [
        'message',
    ]
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
            created_by=self.request.user)  ##添加一个额外的过滤条件 必须是创建者用户

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.updated_by = self.request.user
        post.save()
        return redirect(
            'topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
