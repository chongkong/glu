import argparse
import json
import yaml
import os
import logging
from collections import OrderedDict
from glu.util import OrderedDictYamlLoader

from glu import create_scope


def load_file(path):
    if path.lower().endswith('.yml') or path.lower().endswith('.yaml'):
        with open(path, 'r') as f:
            return yaml.load(f, Loader=OrderedDictYamlLoader)

    else:
        with open(path, 'r') as f:
            return json.load(f, object_pairs_hook=OrderedDict)


def load_scope_from_file(scope, file_uri):
    path = file_uri
    params = {}
    if '?' in file_uri:
        path, params = file_uri.split('?')
        params = dict(tuple(field_and_value.split('='))
                      for field_and_value in params.split('&'))

    scope.load(load_file(path), **params)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, dest='sources', nargs='+', help='Path to the source file')
    parser.add_argument('-e', '--use-env', action='store_true', help='Use environment variable')
    parser.add_argument('-t', '--template', required=True, help='Path to the template file')
    parser.add_argument('-o', '--output', required=True, help='Path for output file')
    return parser.parse_args()


def main():
    args = parse()
    scope = create_scope()

    if args.use_env:
        scope.load(dict(os.environ.items()), load_to='@env')

    for file_uri in args.sources:
        load_scope_from_file(scope, file_uri)

    template = load_file(args.template)
    res = scope.glue(template)

    logging.info('Result:\n{}'.format(json.dumps(res, indent=2)))

    with open(args.output, 'w') as f:
        json.dump(res, f, indent=2, separators=(',', ': '))
        f.write('\n')
