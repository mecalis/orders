from django.shortcuts import render, redirect
from .models import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserForm
from django.views.generic import View
from .forms import ProfileForm

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
    template_name = 'profiles/main.html'

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