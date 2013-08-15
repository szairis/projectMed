from blog.models import Blog
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    list_filter = ['date_created']

admin.site.register(Blog, BlogAdmin)
