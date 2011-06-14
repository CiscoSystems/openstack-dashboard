from optparse import make_option

from django.contrib.auth.forms import PasswordResetForm
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--email', dest='email', default=None,
            help='Specifies the email address for the user.'),
    )
    help = 'Used to change a password.'

    def handle(self, *args, **options):
        email = options.get('email', None)
        template='registration/welcome_to_dair_email.html'
        form = PasswordResetForm({'email': email})
        # TODO: the next 2 lines shouldn't be necessary
        form.cleaned_data = {'email': email} 
        form.clean_email()
        form.save(email_template_name=template)
