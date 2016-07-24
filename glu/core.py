import re
import uuid
from datetime import datetime
from glu.util import get_dot, set_dot_default
from glu.filter import apply_filters, undefined, muted
import time

_scope = {}


def reset_scope(*init, set_basic=True):
    _scope.clear()
    if set_basic:
        _scope['@date'] = datetime.today().strftime('%Y%m%d')
        _scope['@timestamp'] = int(time.time())
        for i in range(10):
            _scope['@uuid_{}'.format(i)] = str(uuid.uuid4())
    for scope in init:
        _scope.update(scope)


def load_scope(scope, load_from=None, load_to=None):
    scope = scope if load_from is None else get_dot(scope, load_from, {})
    load_point = _scope if load_to is None else set_dot_default(scope, load_to, {})
    load_point.update(scope)


def resolve(key, *local_scopes):
    scope = _scope.copy()
    for s in local_scopes:
        scope.update(s)
    res = get_dot(scope, key, undefined)
    return res if res is undefined else glued(res)


def evaluate(expr):
    statement, *filters = (x.strip() for x in expr.split('|'))
    clauses = (x.strip() for x in statement.split('??'))

    res = undefined
    for clause in clauses:
        key, *scopes = (x.strip() for x in clause.split('<'))
        res = resolve(key, *scopes)
        if res is not undefined:
            break

    res = apply_filters(res, *reversed(filters))
    if res is undefined:
        last_key = clauses[-1].split('<')[0].strip()
        raise KeyError('Cannot find key {}'.format(last_key))
    return res


def interpolate(pattern):
    rendered = pattern
    for template in re.findall('{{[^{}]+?}}', pattern):
        expr = template[2:-2].strip()
        res = evaluate(expr)
        assert isinstance(res, (int, str)), (
            'Cannot interpolate {} (={});'
            ' Only int or str value is allowed').format(template, res)
        rendered = rendered.replace(template, res)
    return rendered


def glued(value):
    if isinstance(value, list):
        return [glued(item) for item in value
                if item is not muted]
    if isinstance(value, dict):
        return type(value)([(k, glued(v)) for k, v in value.items()
                            if v is not muted])
    if isinstance(value, str):
        match = re.match('^{{([^{}]+)}}$', value)
        if match is not None:
            return evaluate(match.group(1))
        return interpolate(value)
    return value
