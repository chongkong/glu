import yaml
from collections import OrderedDict


class OrderedDictYamlLoader(yaml.Loader):
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))

OrderedDictYamlLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping)


def head_tail(iterable):
    """ For python2 compatibility """
    lst = list(iterable)
    return lst[0], lst[1:]


def tail_head(iterable):
    """ For python2 compatibility """
    lst = list(iterable)
    return lst[:-1], lst[-1]


def get_dot(dic, key, default=None):
    """ Similar to dict.get(), but key is given with dot (eg. foo.bar) and
    result is evaluated in generous way. That is, get_dot(dic, 'foo.bar.vaz')
    will return dic['foo']['bar'] if both dic['foo'] and dic['foo']['baz'] exists,
    but return default if any of them does not exists.
    """
    keys = key.split('.')
    res = dic
    for k in keys:
        if not isinstance(res, dict):
            return default
        elif k in res:
            res = res[k]
        else:
            return default
    return res


def set_dot_default(dic, key, value):
    """ Similar to dict.set_default(), but key is given with dot (eg. foo.bar)
    Refer docs of get_dot() for more detail. """
    keys, last_key = tail_head(key.split('.'))
    res = dic
    for k in keys:
        if not isinstance(res, dict):
            raise ValueError('Cannot access {}: {} is not a dictionary'.format(key, k))
        res.setdefault(k, {})
        res = res[k]
    if last_key not in res:
        res[last_key] = value
    return res[last_key]


if __name__ == '__main__':
    dic = {}
    set_dot_default(dic, 'a.b.c.d', 'hello')
    hello = get_dot(dic, 'a.b.c.d')
    assert hello == 'hello', 'hello != {}'.format(hello)
