import re
from functools import wraps

undefined = object()
muted = object()
filters = {}


def ensure_string(string):
    assert isinstance(string, (int, str)), 'Cannot apply filter to non-string value {}'.format(string)
    return str(string)


def string_filter(func):
    @wraps(func)
    def wrapper(string):
        if string is undefined or string is muted:
            return string
        return func(ensure_string(string))

    filters[func.__name__] = wrapper
    return wrapper


def mute_filter(cond):
    @wraps(cond)
    def wrapper(variable):
        return muted if cond(variable) else variable

    filters[cond.__name__] = wrapper
    return wrapper


@string_filter
def tokenize(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    return re.compile('[\s_-]+').split(string)


@string_filter
def display(string):
    return ' '.join(token[0].upper() + token[1:] for token in tokenize(string))


@string_filter
def capitalize(string):
    return string[0].upper() + string[1:].lower()


@string_filter
def pascal_case(string):
    return ''.join(capitalize(token) for token in tokenize(string))


@string_filter
def camel_case(string):
    pascal = pascal_case(string)
    return pascal[0].lower() + pascal[1:]


@string_filter
def snake_case(string):
    return '_'.join(token.lower() for token in tokenize(string))


@string_filter
def lisp_case(string):
    return '-'.join(token.lower() for token in tokenize(string))


@string_filter
def uppercase(string):
    return '_'.join(token.upper() for token in tokenize(string))


@string_filter
def uppercase_dash(string):
    return '-'.join(token.upper() for token in tokenize(string))


@string_filter
def capitalize_dash(string):
    return '-'.join(capitalize(token) for token in tokenize(string))


@mute_filter
def mute(variable):
    return variable is undefined


@mute_filter
def mute_if_undefined(variable):
    return variable is undefined


@mute_filter
def mute_if_empty(variable):
    if hasattr(variable, '__len__'):
        return len(variable) == 0
    return False


def apply_filters(item, *exprs):
    for expr in exprs:
        key, *args = expr.split()
        assert key in filters, 'Unknown filter {}'.format(key)
        item = filters[key](item, *args)

    return item
