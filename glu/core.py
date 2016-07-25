import re
import uuid
from datetime import datetime
from glu.util import get_dot, set_dot_default
from glu.filter import apply_filters, undefined, muted
import time


class Scope(object):
    def __init__(self):
        self.scope = {}

    def reset(self, *init, set_basic=True):
        self.scope.clear()
        if set_basic:
            self.scope['@date'] = datetime.today().strftime('%Y%m%d')
            self.scope['@timestamp'] = int(time.time())
            for i in range(10):
                self.scope['@uuid_{}'.format(i)] = str(uuid.uuid4())
        for scope in init:
            self.scope.update(scope)

    def load(self, scope, load_from=None, load_to=None):
        scope = scope if load_from is None \
            else get_dot(scope, load_from, {})
        load_point = self.scope if load_to is None \
            else set_dot_default(self.scope, load_to, {})
        load_point.update(scope)

    def copy(self):
        scope = Scope()
        scope.scope = self.scope.copy()
        return scope

    def override(self, *scope_keys):
        scope = self.copy()
        for s in scope_keys:
            if s not in scope.scope:
                raise KeyError('Undefined scope key: {}'.format(s))
            scope.load(scope.scope[s])
        return scope

    def resolve(self, key):
        res = get_dot(self.scope, key, undefined)
        if res is undefined:
            return undefined
        return self.glue(res)

    def evaluate(self, expr):
        statement, *filters = (x.strip() for x in expr.split('|'))
        clauses = [x.strip() for x in statement.split('??')]

        res = undefined
        for clause in clauses:
            key, *scopes = [x.strip() for x in clause.split('<')]
            res = (self if len(scopes) == 0
                   else self.override(*scopes)).resolve(key)
            if res is not undefined:
                break

        res = apply_filters(res, *reversed(filters))
        if res is undefined:
            last_key = clauses[-1].split('<')[0].strip()
            raise KeyError('Cannot find key {}'.format(last_key))
        return res

    def interpolate(self, pattern):
        rendered = pattern
        for template in re.findall('{{[^{}]+?}}', pattern):
            expr = template[2:-2].strip()
            res = self.evaluate(expr)
            assert isinstance(res, (int, str)), (
                'Cannot interpolate {} (={});'
                ' Only int or str value is allowed').format(template, res)
            rendered = rendered.replace(template, str(res))
        return rendered

    def glue(self, value):
        if isinstance(value, list):
            return [self.glue(item) for item in value
                    if item is not muted]
        if isinstance(value, dict):
            return type(value)([
                                   kv for kv in [(k, self.glue(v)) for k, v in value.items()]
                                   if kv[1] is not muted])
        if isinstance(value, str):
            match = re.match('^{{([^{}]+)}}$', value)
            if match is not None:
                return self.evaluate(match.group(1))
            return self.interpolate(value)
        return value


def create_scope(*init, set_basic=True):
    scope = Scope()
    scope.reset(*init, set_basic=set_basic)
    return scope
