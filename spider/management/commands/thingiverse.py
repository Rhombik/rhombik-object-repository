from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.contrib.auth.models import User

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-u', '--user',
            action='store',
            dest='user',
            help='Attach to partiular user name'),
        make_option('-i', '--user-id',
            action='store',
            dest='user_id',
            help='Attach to partiular user by PK'),
        )
    def handle(self, *args, **options):
        if all([options['user'], options['user_id']]):
            print('You can\'t specify both a user name and a user ID at the same time')
            return
        if options['user']:
            user = User.objects.get(username=options['user'])
        if options['user_id']:
            user = User.objects.get(pk=options['user_id'])
        print(user)
