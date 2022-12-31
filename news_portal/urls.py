from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostFilterList, PostDetail, PostCreate, PostUpdate, PostDelete
from .models import Post


news_urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('search', PostFilterList.as_view(), name='post_search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), {'type': Post.NEWS}, name='news_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]

articles_urlpatterns = [
    path('create/', PostCreate.as_view(), {'type': Post.ARTICLE}, name='article_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]
