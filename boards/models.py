from django.db import models
from django.utils.text import Truncator
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
from markdown import markdown
from django.utils.html import  mark_safe
import  math


class Board(models.Model):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

class Topic(models.Model):
    subject = models.CharField(max_length=200)
    last_updated= models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,related_name = 'topics')
    starter = models.ForeignKey(User,related_name="topics")

    views =models.PositiveIntegerField(default=0) #页面浏览数  整数
    
    def __str__(self):
        return self.subject
        # return "%s : %s by %s"%(self.board,self.subject,self.starter)
    
    def get_page_count(self):
        count = self.posts.count()
        pages = count/20
        # paginate_by = 20
        return math.ceil(pages)
    
    def has_many_pages(self,count = None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if count>6:
            return range(1,5)
        return range(1,count+1)
    
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,related_name = 'posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null = True)  # 可以为空 没有被更新过
    created_by = models.ForeignKey(User,related_name='posts')
    updated_by = models.ForeignKey(User,null = True,related_name='+') #可以为空 同上

    def __str__(self):
        truncated_msg = Truncator(self.message)
        return truncated_msg.chars(30)
        # return self.message[:10]
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message,safe_mode='escape'))

    
    
    