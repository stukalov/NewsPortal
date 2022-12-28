from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostFilterList, PostDetail


urlpatterns = [
   path('', PostList.as_view()),
   path('search', PostFilterList.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
]