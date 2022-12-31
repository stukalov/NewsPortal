from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )

    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория:',
        empty_label='любая',
    )

    created_after = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        label='Новости опубликованные после:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': [],
    #         'category': [],
    #         'created': [],
    #     }

