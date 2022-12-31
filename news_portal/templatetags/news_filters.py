from django import template
import re

register = template.Library()


@register.filter()
def date_formatter(value, format_str=" %d %b %Y"):
    return value.strftime(format_str)


@register.filter()
def news_censor(value):
    # список слов запрещенных к публикации
    # для теста взяты слова из текста ID:3
    list = [
        'оказывается',
        'правильного',
        'упражнения',
        'исправно',
    ]
    regexp = '|'.join(list)

    def replace(value):
        s = value[0]
        mid = '*' * (len(s) - 1)
        return f'{s[0]}{mid}{s[-1]}'

    return re.sub(regexp, replace, value, flags=re.IGNORECASE)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()