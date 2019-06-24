from django.core.management.base import BaseCommand,CommandError
from django.core.management import call_command

from boards.models import Board,Topic,Post,User


class Command(BaseCommand):
    help = ''
    leave_locale_alone  =True
    def handle(self, *args, **options):
        print('start create topics')

        user = User.objects.first()
        board = Board.objects.get(name='Django')
        

        for i in range(100):
        
            subject = f'Topic test #{i}'
            topic = Topic.objects.create(
            subject=subject, board=board, starter=user)
            Post.objects.create(message="Lorem",created_by=user,topic = topic)
