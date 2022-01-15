from django.contrib import admin
from .models import Article, Comments, Connection

admin.site.register(Article)
admin.site.register(Comments)
admin.site.register(Connection)

