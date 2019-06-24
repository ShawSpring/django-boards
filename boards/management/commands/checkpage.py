from django.core.management.base import BaseCommand,CommandError
from django.core.management import call_command
from boards.models import Board,Topic,Post,User
from django.core.paginator import Paginator

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        
        topics_count =Topic.objects.count()
        print(f"topics count:{topics_count}")

        Django_topics_count =  Topic.objects.filter(board__name='Django').count()
        print(f"Django board topics count:{Django_topics_count}")

        query_set = Topic.objects.filter(board__name='Django').order_by('-last_updated')
        print("query_set: django board topics oreder by -last_updated")
        for query in query_set:
            print(query)
        
        print('-----------------paginator------------------')
        paginator = Paginator(query_set,20)
        print(paginator.count) #总元素数量
        print(paginator.num_pages)  #页面数  
        print(paginator.page_range)
        print('---------------- page(2)---------------------') 
        page = paginator.page(2)
        print(page)
        for i  in page:
            print(i)
        print('has_next',page.has_next())
        print('has_previous',page.has_previous())
        print('has ohter pages',page.has_other_pages())
        print('previous page number',page.previous_page_number())
        
        print(type(page))
        print(type(paginator))

        print(f'-------------page({paginator.num_pages})-----------------------')
        page = paginator.page(paginator.num_pages)
        print(page)
        print(page.has_next())
        

        print(paginator.page(7)) # 看看不存在的页面 抛出 EmptyPage