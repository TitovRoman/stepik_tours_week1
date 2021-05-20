from django import template

register = template.Library()


@register.filter()
def ru_pluralize(number, arg: str = 'ночь,ночи,ночей'):
    nominative_singular, genitive_singular, genitive_plural = arg.split(',')
    number = abs(number)

    if number % 10 in [0, 5, 6, 7, 8, 9] or 11 <= number % 100 <= 19:
        return f'{number} {genitive_plural}'
    elif number % 10 == 1:
        return f'{number} {nominative_singular}'
    else:
        return f'{number} {genitive_singular}'
