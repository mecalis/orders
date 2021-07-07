from django.shortcuts import render, redirect
from .models import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserForm
from django.views.generic import View
from .forms import ProfileForm


# REG EMAIL segítségével
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

# REG GMAIL - EMAIL segítségével
from django.contrib import messages
from django.core.mail import send_mail
# from django.shortcuts import render, redirect
from django.conf import settings


#activate
# from django.contrib.auth import login
from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
# from .tokens import account_activation_token

# Create your views here.
@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    confirm = False
    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/main.html', context)

class UserFormView(View):
    form_class = UserForm
    template_name = 'profiles/register.html'

    #kap az ember egy üres formot
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form} )
    #miután megnyomta a gombot
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)

            # adat tisztítás
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                return redirect('orders:home')
        return render(request, self.template_name, {'form': form})


def signup(request):
    template_name = 'profiles/register.html'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Felhasználói név aktiválása.'
            message = render_to_string('profiles/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            recipient = user.email
            send_mail(subject,
                      message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, 'Success!')

            # user.email_user(subject, message)
            # print("email után")




            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, template_name, {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('orders:home')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'profiles/account_activation_sent.html')

# pass teszttesztteszt
