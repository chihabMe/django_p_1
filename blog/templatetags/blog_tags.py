from django import template 
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown



register = template.Library()

@register.filter(name="allFirstToCapital")
def capitalize(text):
    string = text.split(" ")
    for i in range(len(string)):
        string[i]=string[i].capitalize()
    return ' '.join(string)
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def get_most_commented_posts(count = 4 ):
    return Post.published.annotate(total_comments=Count('post_comments')).order_by('-total_comments')[:count]
    
@register.inclusion_tag('blog/latest_posts.html')
def latest_posts(count = 5 ):
    latest = Post.published.order_by('-publish','title')[:count]

    return {"latest_posts":latest}
@register.simple_tag 
def total_posts():
    total = Post.published.count()
    return  total