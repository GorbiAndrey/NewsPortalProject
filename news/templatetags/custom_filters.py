from django import template

register = template.Library()

censor_list = ['bad_word_1', 'bad_word_2', 'bad_word_3']
#список плохих слов, по которым будет проводиться сравнение в название новости и тексте

@register.filter(name='censor')
def censor(title=""):
    new_title = ""

    for word in title.split():
        if word in censor_list:
            new_title += '* '
        else:
            new_title += word + ' '

    return new_title