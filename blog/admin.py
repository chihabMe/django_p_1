from django.contrib import admin
from .models import Post,Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):

    list_display = ('title','created','updated','user','active')
    list_filter = ('active','created')
    search_fields = ('title','body','email')
    raw_id_fields = ('user',)
    ordering = ('created','title')
    date_hierarchy = ('created')

admin.site.register(Comment,CommentAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','publish','status')
    list_filter = ('status','author','publish')
    search_fields=('title',)
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author',)  
    ordering=('status','publish')
    date_hierarchy=('publish')
    
admin.site.register(Post,PostAdmin)