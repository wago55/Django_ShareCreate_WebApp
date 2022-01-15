from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView, View, ListView
from django.views.generic.edit import ModelFormMixin

from .models import Article, Comments, Connection, User
from .forms import ArticleForm, CommentsForm

from taggit.models import Tag


class CreateArticleView(CreateView, LoginRequiredMixin):
    form_class = ArticleForm
    model = Article
    template_name = "share_create/create_article.html"
    success_url = reverse_lazy('accounts:list_profile')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.user = self.request.user
        article.created_by = self.request.user.username

        article.save()
        messages.success(self.request, '記事の作成が完了しました。')
        return super().form_valid(form)


class UpdateArticleView(UpdateView, LoginRequiredMixin):
    form_class = ArticleForm
    model = Article
    template_name = "share_create/update_article.html"
    success_url = reverse_lazy('accounts:list_profile')


class DetailArticleView(ModelFormMixin, DetailView):
    template_name = "share_create/detail_article.html"
    model = Article
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
        context = super(DetailArticleView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(article_id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.article_id = self.kwargs['pk']
            comment.commented_by = self.request.user.username
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save()
        comment.user = self.request.user
        comment.commented_by = self.request.user.username
        comment.article_id = self.kwargs['pk']

        comment.save()
        messages.success(self.request, 'コメントの送信が完了しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("share_create:detail_article", kwargs={'pk': self.object.article.pk})


class FavBase(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['pk'])

        if self.request.user in article.fav.all():
            obj = article.fav.remove(self.request.user)
        else:
            obj = article.fav.add(self.request.user)

        return obj


class FavHomeView(FavBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return redirect('accounts:home')


class FavDetailView(FavBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']

        return redirect('share_create:detail_article', pk)


class DeleteArticleView(DeleteView, LoginRequiredMixin):
    model = Article
    template_name = "share_create/delete_article.html"
    success_url = reverse_lazy('accounts:list_profile')


class CreateCommentsView(CreateView):
    model = Comments
    template_name = "share_create/detail_article.html"
    # success_url = reverse_lazy("share_create:detail_article")
    form_class = CommentsForm

    def form_valid(self, form, *args, **kwargs):
        comments = form.save(commit=False)
        comments.user = self.request.user
        comments.commented_by = self.request.user.username
        comments.article_id = self.kwargs['article_id']
        comments.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("share_create:detail_article", kwargs={'pk': self.object.article.pk})


class DeleteCommentsView(DeleteView, LoginRequiredMixin):
    model = Comments
    template_name = "share_create/delete_comment.html"

    # success_url = reverse_lazy('accounts:list_profile')

    def get_success_url(self):
        return reverse("share_create:detail_article", kwargs={'pk': self.object.article.pk})


class FollowBase(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        target_user = User.objects.get(pk=pk)

        my_connection = Connection.objects.get_or_create(user=self.request.user, id=self.request.user.id)

        if target_user in my_connection[0].following.all():
            obj = my_connection[0].following.remove(target_user)

        else:
            obj = my_connection[0].following.add(target_user)

        return obj


class FollowDetail(FollowBase):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        return redirect('accounts:detail_profile', pk)


class FavPageList(ListView):
    template_name = 'share_create/fav_page.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(FavPageList, self).get_context_data(**kwargs)
        context['all_fav_page'] = Article.objects.filter(fav=self.request.user.id)

        return context


class TagsSearch(ListView):
    template_name = 'account/home.html'
    model = Article

    def get_queryset(self):
        result = super(TagsSearch, self).get_queryset()
        query = self.request.GET.get('query')

        if query:
            # tag = Tag.objects.get(name=query)
            # result = Article.objects.filter(tags=tag)
            result = Tag.objects.all()
        return result


