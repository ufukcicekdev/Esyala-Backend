from django.urls import path, include
from blog.views import *


urlpatterns = [
    path('', GetBlogsView.as_view(), name='blog_home'),
    path('blog_categories/', GetBlogsCategoriesView.as_view(), name='blog_categories'),
    path('popular_blogs/', GetPopularBlogsViews.as_view(), name='popular_blogs'),
    path('<slug:slug>/', GetBlogDetailViews.as_view(), name='blog_detail'),
    path('blog_category_product/<slug:slug>/', GetCategoryBlogsViews.as_view(), name='blog_category_product'),
]
