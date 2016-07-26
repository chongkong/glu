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


def get_dot(dic, key, default=None):
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
    *keys, last_key = key.split('.')
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
