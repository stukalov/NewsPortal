from news_portal.models import *
from django.contrib.auth.models import User

root_user = User.objects.get(username='root')

# Создано 2 пользователя Vasja и Petja:
vasja = User.objects.create(username='Vasja')
petja = User.objects.create(username='Petja')

# Создано 2 автора:
a_vasja = Author.objects.create(user=vasja)
a_petja = Author.objects.create(user=petja)

# Создано 5 категории:
c_sport = Category.objects.create(name='Спорт')
c_politics = Category.objects.create(name='Политика')
c_education = Category.objects.create(name='Образование')
c_person = Category.objects.create(name='Персоны')
c_health = Category.objects.create(name='Здоровье')

#Создано 1 новость:
news_1 = Post.objects.create(author=a_vasja, type=Post.NEWS, title='Илон Маск запустил в Twitter опрос о помиловании Ассанжа и Сноудена', body='Владелец Twitter подчеркнул, что не выражает свое мнение, но обещал провести опрос о помиловании экс-сотрудника АНБ США Сноудена и основателя WikiLeaks Ассанжа. Большинство опрошенных высказались за их помилование')

# Создано 2 статьи:
article_1 = Post.objects.create(author=a_vasja, type=Post.ARTICLE, title='Как сесть на шпагат', body='Шпагат - это показатель гибкости. Он используется в гимнастике, в танцах, в боевых искусствах, в чирлидинге и т.д. Шпагат одним дается легко, другим - трудно. Но при правильной постановке цели освоить это упражнение вполне можно за одну неделю. Правда, при одном условии, придется методично и серьезно работать.')
article_2 = Post.objects.create(author=a_petja, type=Post.ARTICLE, title='Упражнения для улучшения пищеварения', body='Есть упражнения от болей в спине, в шее, от головных болей и от болей в суставах рук и ног и зарядка для глаз. Оказывается, для желудка тоже есть зарядка и улучшить пищеварение можно не только с помощью правильного питания или специальных пищевых добавок. В йоге как раз есть упражнения, которые помогают нашей пищеварительной системе работать исправно.')

# Присвоение категорий:
PostCategory.objects.create(post=news_1, category=c_politics)
PostCategory.objects.create(post=news_1, category=c_person)
PostCategory.objects.create(post=article_1, category=c_sport)
PostCategory.objects.create(post=article_1, category=c_education)
PostCategory.objects.create(post=article_2, category=c_health)
PostCategory.objects.create(post=article_2, category=c_sport)

# Создание комментариев:
comment_1 = Comment.objects.create(post=news_1, user=root_user, body='Комментарий 1')
comment_2 = Comment.objects.create(post=news_1, user=vasja, body='Комментарий 2')
comment_3 = Comment.objects.create(post=article_1, user=vasja, body='Комментарий 3')
comment_4 = Comment.objects.create(post=article_1, user=petja, body='Комментарий 4')
comment_5 = Comment.objects.create(post=article_2, user=petja, body='Комментарий 5')
comment_6 = Comment.objects.create(post=article_2, user=root_user, body='Комментарий 6')

# Проставляем Лайки случайным образом:
from random import choice, randrange
[news_1.like() for _ in range(randrange(20)) if choice([0,1]) == 0]
[news_1.dislike() for _ in range(randrange(20)) if choice([0,1]) == 0]
[article_1.like() for _ in range(randrange(20)) if choice([0,1]) == 0]
[article_1.dislike() for _ in range(randrange(20)) if choice([0,1]) == 0]
[article_2.like() for _ in range(randrange(20)) if choice([0,1]) == 0]
[article_2.dislike() for _ in range(randrange(20)) if choice([0,1]) == 0]

[comment_1.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_1.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_2.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_2.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_3.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_3.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_4.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_4.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_5.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_5.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_6.like() for _ in range(randrange(10)) if choice([0,1]) == 0]
[comment_6.dislike() for _ in range(randrange(10)) if choice([0,1]) == 0]

# Обновляем рейтинг авторов
a_vasja.update_rating()
a_petja.update_rating()

# автор с самым большим рейтингом
author = Author.objects.order_by('-rate')[0]
print(author.user.username)
print(author.rate)

# вывод даты добавления, username автора, рейтинга, заголовка и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
article = Post.objects.filter(type=Post.ARTICLE).order_by('-rate')[0]
print(article.author.user.username)
print(article.rate)
print(article.title)
print(article.preview())

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = article.comment_set.all()
for comment in comments:
    print(comment.created)
    print(comment.user.username)
    print(comment.rate)
    print(comment.body)



