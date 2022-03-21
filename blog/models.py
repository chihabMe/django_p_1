from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse 

from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
	STATUS_CHOUICES =(

		('draft','Draft'),
		('published','Published')
		)	
	title = models.CharField(max_length=300)
	body = models.TextField(null=True)
	slug = models.SlugField(max_length=300,unique_for_date='publish')
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
	publish = models.DateTimeField(default=timezone.now())
	status = models.CharField(max_length=10,choices=STATUS_CHOUICES,default='draft')

	objects  = models.Manager()
	published = PublishedManager()


	##adding a third apary taggin manager 
	tags = TaggableManager()

	def __str__(self):
		return self.title[0:20]

	
	def get_absolute_url(self):
		return reverse('blog:post_details',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
	class Meta:

		ordering = ('-publish',)
class ActiveCommentManager(models.Manager):
	def get_queryset(self):
		return super(ActiveCommentManager,self).get_queryset().filter(active=True)
class Comment(models.Model):
	title = models.CharField(max_length=100)
	body = models.TextField()
	email = models.EmailField()
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comments')
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	objects = models.Manager()
	ActiveManager = ActiveCommentManager()
	class Meta:
		ordering = ("created",)
	def __str__(self):
		return self.user.username +" on "+self.post.title[0:20]
	