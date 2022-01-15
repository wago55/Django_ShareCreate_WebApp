from .models import Article, Comments
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


# 記事のform
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = (
            'title', 'url', 'tags','description'
        )
        widgets = {
            'description': SummernoteWidget()
        }


# 記事のコメント
class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = (
            'text',
        )