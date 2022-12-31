from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostFilterList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied('Неавторизованный пользователь не может создавать статьи и новости')
        # пользователи Vasja и Petja - авторы - их пароль "qwer1234"
        self.__author = Author.objects.get(user=user.id)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.type = self.kwargs['type']
        self.object.author = self.__author
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied('Неавторизованный пользователь не может редактровать статьи')
        post = self.model.objects.get(id=self.kwargs['pk'])
        if not user.is_superuser and post.author.user != user:
            raise PermissionDenied('Редактровать статьи может только автор или суперюзер')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_search')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied('Неавторизованный пользователь не может удолять статьи')
        post = self.model.objects.get(id=self.kwargs['pk'])
        if not user.is_superuser and post.author.user != user:
            raise PermissionDenied('Удолять статьи может только автор или суперюзер')


