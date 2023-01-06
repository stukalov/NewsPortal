from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
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


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = 'news_portal.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except ObjectDoesNotExist:
            author = Author.objects.create(user=user)
        self.object = form.save(commit=False)
        self.object.type = self.kwargs['type']
        self.object.author = author
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = 'news_portal.edit_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = 'news_portal.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_search')


