# Glu

Simple config file generation library. Glu refers to *glue*ing variables and templates.

Glu is simple python library to make your config configurable. Sometimes config files are largely 
duplicated, differ a little. You can apply DRY principle for that. You might use a template engines
like Jinja, or make a simple code for configuring. But Jinja template is not optimized for configuration,
and writing extra code makes you tired.
 
And Glu appeared from lack and the need of configuration-optimized template engine. Glu uses
template syntax that is similar to Jinja, but provides much robust syntax for configuration hierarchy.
With Glu, you can keep your any kind of config files DRY

## How to install?

Support any python version. If you are having an compatibility issue, please let me know.

```
pip install glu
```

## Quick Start

You need context, or `Scope` to generate template file with variables. Glu provides `Scope` object
so that you can load scope and inject variables using scope. Simple usage is:

``` python
from glu import create_scope

scope = create_scope()
scope.load({ 'greeting': 'Hello, Glu!' })
print(scope.glue('{{ greeting }}'))  # will print 'Hello, Glu!'
```

It's syntax similar to other template engines like jinja.

``` python
scope.load({
    'name': 'World'
})

scope.glue({
    'greeting': 'Hello, {{ name }}'
})

# will be
{
    'greeting': 'Hello, World'
}
```

If template expression is used solely (not interpolated), its value is inserted, whatever value type is.
Also you can access nested scope using `.`

``` python

scope.load({
    'counting': {
        'number': [1, 2, 3],
        'english': ['one', 'two', 'three']
    }
})

scope.glue({
    '123': '{{ counting.number }}',
    'one_two_three': '{{ counting.english }}'
})

# will be
{
    '123': [1, 2, 3],
    'one_two_three': ['one', 'two', 'three']
}

```

You can also specify loading point using `load_from` and `load_to` keyword argument

``` python
scope.load({
    'score': {
        'math': 93
    }
}, load_from='score', load_to='midterm_score')

scope.glue('{{ midterm_score.math }}')  # will be 93

```

You can specify fallback value using `??`, which will be used when former variable is undefined

``` python
scope.load({
    'score': {
        'math': 93
    }
})

scope.glue('{{ score.science ?? score.history ?? score.math }}')  # will be 93
```

You can apply some filters

``` python
scope.load({
    'foo': 'This_isREALLYAmazing'
})

scope.glue({
    'display': '{{ foo | display }}',
    'camel_case': '{{ foo | camel_case }}',
    'pascal_case': '{{ foo | pascal_case }}',
    'snake_case': '{{ foo | snake_case }}',
    'lisp_case': '{{ foo | lisp_case }}',
    'uppercase': '{{ foo | uppercase }}',
    'uppercase_dash': '{{ foo | uppercase_dash }}',
    'capitalize_dash': '{{ foo | capitalize_dash }}',
})

# will be
{
    'display': 'This Is Really Amazing',
    'camel_case': 'thisIsReallyAmazing',
    'pascal_case': 'ThisIsReallyAmazing',
    'snake_case': 'this_is_really_amazing',
    'lisp_case': 'this-is-really-amazing',
    'uppercase': 'THIS_IS_REALLY_AMAZING',
    'uppercase_dash': 'THIS-IS-REALLY-AMAZING',
    'capitalize_dash': 'This-Is-Really-Amazing',
}
```

You can omit the undefined field by using `mute`, or `mute_if_empty` filter

``` python
scope.load({
    'empty_array': [],
    'empty_string': '',
    'empty_dict': {}
})

scope.glue({
    'foo': '{{ empty_array | mute_if_empty }}',
    'bar': '{{ empty_string | mute_if_empty }}',
    'zoo': '{{ empty_dict | mute_if_empty }}',
    'coz': '{{ undefined_var | mute }}'
})

# will be an empty dict
{}
```

And last, you can insert temporal scope for resolving expression, which enables to
use template as a function. This scope injection is the key feature of Glu.

``` python
scope.load({
    'greeting': 'hello, {{ name }}'
})

scope.load({
    'foo_scope': {
        'name': 'foo'
    },
    'bar_scope': {
        'name': 'bar'
    }
})

scope.glue({
    'hello_foo': '{{ greeting < foo_scope }}',
    'hello_bar': '{{ greeting < bar_scope }}'
})

# will be
{
    'hello_foo': 'hello, foo',
    'hello_bar': 'hello, bar'
}
```

Following basic variables are registered as default. You can disable registration of basic variables
by calling `create_scope(set_basic=False)`

| Variable Name | Value |
| ----- | ----- |
| @date | date string of format `yyyymmdd` |
| @timestamp | int value of unix timestamp |
| @uuid_x | randomly issued UUID string. There are total 10 random uuid: `@uuid_0` to `@uuid_9` |

## Command Line Interface

Once you've installed Glu via pip, you can use simple command line interface that Glu provides.
It supports only one syntax:

``` shell
$ glu --load-scope scope_file [scope_file...] --target target_file --output output_file [--use-env] [--output-format format]
```

Or simply, 

```
$ glu -s scope_file [scope_files...] -t target_file -o output_file [-e] [-f format]
```
 

| Argument | Description | Type |
| ----- | ----- | ----- | ----- |
| _scope_file_ | List of path to json or yaml files, which will be loaded by `scope.load()` | Path |
| _target_file_ | Path to json or yaml file to be glued via `scope.glue()` | Path |
| _output_file_ | Path to json or yaml file that is generated by `scope.glue()` | Path |
| _--use-env_ | whether to load environment variable into scope |  |
| _--output-format_ | Specify output format of _output_file_ (`json` or `yaml`) | `json` or `yaml` |

Since you can add `load_from` and `load_to` parameters to `scope.load()`, You can also use such 
parameters in _scope_file_ by querystring. Let's look at the example:

``` shell
$ glu -s /path/to/file.json?load_from=foo.bar&load_to=baz\
         /path/to/yaml_file.yml?load_to=foo 
      -t /path/to/target_file.json
      -o /path/to/output_file.json
      --use-env
```
