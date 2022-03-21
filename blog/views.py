from django.shortcuts import render,get_object_or_404 
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.views.generic import ListView
from .models import Post,Comment 
from .forms import EmailPostForm,CommentForm

##django aggregation 

from django.db.models import Count
##

from django.core.mail import send_mail

##third pary taggin app 
from taggit.models import Tag
# Create your views here.
##adding search 
from django.contrib.postgres.search import SearchVector ,SearchQuery,SearchRank
from django.contrib.postgres.search import TrigramSimilarity
##
def post_search(request):
    q = request.GET.get('q')
    posts = None 
    if q:
        search_query = SearchQuery(q)
        search_vector = SearchVector('title',weight='A')+SearchVector('body',weight='B')
        
        # posts = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
        # posts = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        
        posts = Post.published.annotate(similarity = TrigramSimilarity('title',q )).filter(similarity__gt=0.1).order_by("-similarity")
    else:
        q='None'
    context = {
        'posts':posts,
        'query':q

    }
    return render(request, 'blog/post_list.html',context) 
def post_list_by_tag(request,tag_slug=None):
    object_lst = Post.published.all()
    pots = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_lst = object_lst.filter(tags__in=[tag])
        posts = object_lst
    context = {
        'posts':posts

    }
    return render(request, 'blog/post_list.html',context)    
def post_share(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    form = EmailPostForm(request.POST or None)
    sent = False 
    if request.method=='POST':
        if form.is_valid():
            data = form.cleaned_data 
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends  you to read this post ' {post.title}' "
            message = f"read it from here {post_url} \n\n {data['name']} says this about it  \n\n------------------\n\n{data['comments']}\n\n------------------"
            my_email = 'chihab.me.dev@gmail.com'
            to = data['to']
            send_mail(subject, message, my_email,[to], fail_silently=False)
            sent = True 
            form = EmailPostForm()
    context = {
        'post':post,
        'form':form,
        'sent':sent
    }
    return render(request,'blog/post_share.html',context)
class PostListPage(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2 ; 
    template_name = 'blog/post_list.html'
def post_list_page(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try :
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context  = {
        "posts":posts,
        'posts':posts
    }
    return render(request,'blog/post_list.html',context)
def post_details_page(request,year,month,day,slug):
    obj =  get_object_or_404(Post,slug=slug,publish__year=year,publish__month=month,publish__day=day,status='published')
    comments =  obj.post_comments.filter(active=True)
    form = CommentForm(request.POST or None )
    new_comment =None
    ##adding recommendation system 
    post_tags_ids = obj.tags.values_list("id",flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)
    similar_posts=similar_posts.exclude(id=obj.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by("-same_tags",'-publish')[0:6]
    
    ###
    if request.method=='POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post  = obj 
            new_comment.user = request.user 
            new_comment.save()
            form = CommentForm()
     
    context = {
        'post':obj ,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':form,
        'similar_posts':similar_posts
    }
    return render(request,'blog/detail.html',context)