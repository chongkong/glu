import argparse
import requests
import json
import yaml
import functools
import os
import logging

from glu import create_scope


def load_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)


def load_yaml_file(path):
    with open(path, 'r') as f:
        return yaml.load(f)


def load_json_from_http(url, method='get', **kwargs):
    return requests.request(method, url, **kwargs).json()


def load_scope(scope, scope_provider, *args, load_from=None, load_to=None, **kwargs):
    scope.load(scope_provider(*args, **kwargs),
               load_from=load_from, load_to=load_to)


def save_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f)


def save_yaml(path, obj):
    with open(path, 'w') as f:
        yaml.dump(obj, f)


def parse():
    parser = argparse.ArgumentParser()
    func_help_fmt = '''Load {} from file, remote http server, or
                    custom variable defined from shell.

                    eg.
                        json('/path/to/scope_file.json',load_from='foo.bar')
                        yaml('/path/to/scope_file.yml',load_to='voo.baz')
                        http('https://google.com',params={'q':'¯\_(ツ)_/¯'})
                        var(varKey='¯\_(ツ)_/¯')

                    Note that you cannot use space within each argument. If you want
                    to use space in value, use '\s' instead. Each argument will be
                    evaluated using python eval()'''

    parser.add_argument('-l', '--load-scope', required=True, dest='scopes', nargs='+', help=func_help_fmt.format('scope'))
    parser.add_argument('-e', '--use-env', action='store_true', help='Use environment variable')
    parser.add_argument('-t', '--target', required=True, help=func_help_fmt.format('target'))
    parser.add_argument('-o', '--output', required=True, help='Path to output file')
    parser.add_argument('-f', '--output-format', choices=['json', 'yaml'], help='Format of output file')

    return parser.parse_args()


def create_eval_context(scope=None):
    eval_ctx = dict(globals().items())
    for key in list(eval_ctx.keys()):
        if key not in ['__builtins__', 'sys']:
            eval_ctx.pop(key)

    if scope is not None:
        eval_ctx.update({
            'json': functools.partial(load_scope, scope, load_json_file),
            'yaml': functools.partial(load_scope, scope, load_yaml_file),
            'http': functools.partial(load_scope, scope, load_json_from_http),
            'var': functools.partial(load_scope, scope, dict)
        })
    else:
        eval_ctx.update({
            'json': load_json_file,
            'yaml': load_yaml_file,
            'http': load_json_from_http,
            'var': dict
        })

    return eval_ctx


def main():
    args = parse()
    scope = create_scope()
    scope_eval_ctx = create_eval_context(scope)
    target_eval_ctx = create_eval_context()

    if args.use_env:
        scope.load(dict(os.environ.items()))

    for scope_expr in args.scopes:
        eval(scope_expr.replace('\s', ' '), scope_eval_ctx)

    target = load_json_file(
        eval(args.target.replace('\s', ' '), target_eval_ctx))
    res = scope.glue(target)

    logging.info('Result:\n{}'.format(json.dumps(res, indent=2)))

    if args.output_format == 'json':
        save_json(args.output, res)
    elif args.output_format == 'yaml':
        save_yaml(args.output, res)
    elif args.output.endswith('json'):
        save_json(args.output, res)
    elif args.output.endswith('yml') or args.output.endswith('yaml'):
        save_yaml(args.output, res)
    else:
        save_json(args.output, res)
