from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.SmallIntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3
        aggregate = self.post_set.aggregate(rate=Sum('rate'))
        result = aggregate['rate'] * 3
        # суммарный рейтинг всех комментариев автора;
        aggregate = self.user.comment_set.aggregate(rate=Sum('rate'))
        result += aggregate['rate']
        # суммарный рейтинг всех комментариев к статьям автора.
        aggregate = self.post_set.aggregate(rate=Sum('comment__rate'))
        result += aggregate['rate']
        self.rate = result
        self.save()
        return result


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=ARTICLE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rate = models.SmallIntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self, max_len=124):
        text = self.body
        if len(text) > max_len:
            text = f'{text[:max_len]}...'
        return text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rate = models.SmallIntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()


