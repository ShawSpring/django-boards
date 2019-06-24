from django.core.management.base import BaseCommand,CommandError
from django.core.management import call_command

from boards.models import Board,Topic,Post,User


class Command(BaseCommand):
    help = 'create posts for test'

    leave_locale_alone  =True
    def handle(self, *args, **options):
        print('start create posts')

        user = User.objects.last()
        board = Board.objects.get(name='Django')
        topic = Topic.objects.filter(board=board).last()

        for i in range(50,200):
            message = 'message for test #%s'%i
            Post.objects.create(message = message,topic=topic,created_by = user)
        
        
 