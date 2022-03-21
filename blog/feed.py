from django.shortcuts import render

# Create your views here.
from django.contrib.syndication.views import Feed 
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post 
class LatestPostsFeed(Feed):
    title = 'my own blog'
    link = reverse_lazy('blog:posts_list')
    description = ' ne posts of my blog'
    def items(self):
        return Post.published.all()[:5]
    def item_title(self,item):
        return item.title 
    def item_description(self, item):
        if truncatewords(item.body, 30):
            return truncatewords(item.body, 30)
        return "there is no description "