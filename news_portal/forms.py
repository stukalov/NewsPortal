from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    body = forms.CharField(
        label='Содержание',
        widget=forms.Textarea
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Категория:',
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        if body is not None and len(body) < 20:
            raise ValidationError({
                "body": "Содержание не может быть менее 20 символов."
            })
        return cleaned_data

