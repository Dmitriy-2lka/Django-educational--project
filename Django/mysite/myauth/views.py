from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.views import LogoutView
from django.shortcuts import reverse, get_object_or_404, redirect

from .models import Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')

        user = authenticate(
            self.request,
            username=username,
            password=password
        )

        login(request=self.request, user=user)

        return response


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/about-me.html"


class NewLogoutView(LogoutView):
    template_name = 'myauth/logout.html'
    http_method_names = ['get', 'post']


class UserUpdateAvatarView(LoginRequiredMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()


        if not (request.user.is_staff or request.user == profile.user):
            return redirect('myauth:about-me')

        return super().dispatch(request, *args, **kwargs)

    model = Profile
    fields = 'bio', 'avatar',
    template_name_suffix = '_update_avatar'
    pk_url_kwarg = 'pk'
    context_object_name = 'profile_detail'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.profile

    def get_success_url(self):
        return reverse('myauth:about-me')


class UsersListView(ListView):
    template_name = 'myauth/users.html'
    model = User
    context_object_name = 'list_users'


class AboutUserView(LoginRequiredMixin, DetailView):
    template_name = "myauth/about-user.html"
    model = User
    context_object_name = 'user_detail'

    def dispatch(self, request, *args, **kwargs):

        try:
            profile = request.user.profile
        except Profile.RelatedObjectDoesNotExist:
            profile = Profile.objects.create(user=request.user)

        if self.kwargs['pk'] == request.user.pk:
            return redirect('myauth:about-me')

        return super().dispatch(request, *args, **kwargs)

