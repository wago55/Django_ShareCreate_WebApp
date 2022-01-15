from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UpdateUserProfileForm, InquiryForm
from .models import User
from share_create.models import Article, Connection

from taggit.models import Tag

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "account/signup.html"
    success_url = reverse_lazy('top')

    # 変換されたformの内容をuserにセットしてログイン処理して、succsess_urlをgetしてHttpresponseで飛ばす
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, "会員登録に成功しました")

        self.object = user

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "会員登録に失敗しました")

        # 失敗したら保存しているformをもう一度入れてそのページを再表示
        return super().form_invalid(form)


class HomeView(ListView):
    template_name = 'account/home.html'
    model = Article

    def get_queryset(self):
        result = super(HomeView, self).get_queryset()
        query = self.request.GET.get('query')

        if query:
            tag = Tag.objects.get(name=query)
            result = Article.objects.filter(tags=tag)

            return result

        else:
            return Article.objects.exclude(created_by=self.request.user.username)


class UpdateProfileView(UpdateView, LoginRequiredMixin):
    template_name = 'account/update_profile.html'
    form_class = UpdateUserProfileForm
    model = User
    success_url = reverse_lazy('accounts:list_profile')


class ListProfileView(ListView, LoginRequiredMixin):
    template_name = 'account/list_profile.html'
    model = User

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(id=self.request.user.id)
        return query

    def get_context_data(self, **kwargs):
        context = super(ListProfileView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(user_id=self.request.user)
        return context


class DetailProfileView(DetailView):
    template_name = 'account/detail_profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(DetailProfileView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(user_id=self.kwargs['pk'])
        context['user'] = User.objects.filter(id=self.kwargs['pk'])
        context['connection'] = Connection.objects.filter(user_id=self.request.user.id)
        return context


class InquiryView(FormView):
    template_name = 'account/inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        form.send_mail()
        messages.success(self.request, 'メッセージを送信しました。')
        return super().form_valid(form)


class FollowList(ListView, LoginRequiredMixin):
    template_name = 'share_create/follow_list.html'
    model = Connection

    def get_queryset(self):
        connection = Connection.objects.get_or_create(user_id=self.request.user.pk)
        all_follow = connection[0].following.all()

        return all_follow


class FollowerList(ListView, LoginRequiredMixin):
    template_name = 'share_create/follower_list.html'
    model = Connection

    def get_queryset(self):

        count = Connection.objects.all().count()
        connection = Connection.objects.all()
        follower = []

        for i in range(count):
            # tmp = connection[i].following.filter(id=self.request.user.id)
            if connection[i].following.filter(id=self.request.user.id):
                follower.append(connection[i].user.username)

        return follower


class FollowListDetail(DetailView, LoginRequiredMixin):
    template_name = 'share_create/follow_list_detail.html'
    model = Connection

    def get_context_data(self, **kwargs):
        context = super(FollowListDetail, self).get_context_data(**kwargs)
        all_follow = Connection.objects.filter(user_id=self.kwargs['pk'])
        context['all_follow'] = all_follow[0].following.all()

        return context


class FollowerListDetail(DetailView, LoginRequiredMixin):
    template_name = 'share_create/follower_list_detail.html'
    model = Connection

    def get_context_data(self, **kwargs):
        context = super(FollowerListDetail, self).get_context_data(**kwargs)
        count = Connection.objects.all().count()
        connection = Connection.objects.all()
        follower = []

        for i in range(count):
            if connection[i].following.filter(id=self.kwargs['pk']):
                follower.append(connection[i].user.username)

        context['all_follower'] = follower

        return context

