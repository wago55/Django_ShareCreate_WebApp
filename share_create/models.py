from django.db import models
from accounts.models import User
from django.shortcuts import reverse
from taggit.managers import TaggableManager


# 記事マネージャー
# class ArticleManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter()
# タグ付け


# 記事のモデル
class Article(models.Model):
    title = models.CharField('タイトル', max_length=50)
    url = models.URLField('URL')
    description = models.TextField('本文', max_length=100000)

    created_by = models.CharField('作成者', max_length=20, null=True)
    created_at = models.DateTimeField('作成時間', auto_now_add=True)
    updated_at = models.DateTimeField('最終更新時間', auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fav = models.ManyToManyField(User, related_name='article_fav', blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'article'


# 記事へのコメント
class Comments(models.Model):
    text = models.TextField('コメント')
    commented_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.CharField('投稿者',  max_length=100, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('share_create:detail_article', kwargs={'pk': self.article.id})

    class Meta:
        db_table = 'comments'


# フォロー関係の構築
class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="follow", blank=True)

    class Meta:
        db_table = 'connection'



