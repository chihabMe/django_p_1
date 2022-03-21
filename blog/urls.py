
from django.urls import path 
from . import views 
from .feed import LatestPostsFeed
app_name = 'blog  ' 

urlpatterns = [
    path('',views.post_list_page,name='posts_list'),
    path('posts/',views.PostListPage.as_view(),name='posts_list_view'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',views.post_details_page,name='post_details'),
    path("share/<int:id>/",views.post_share,name='post_share'),
    path('posts/tag__<slug:tag_slug>',views.post_list_by_tag,name='post_by_slug'),
    path('search/',views.post_search,name='post_search'),

    path('feed/', LatestPostsFeed(), name='post_feed'),
]
