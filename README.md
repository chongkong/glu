# Glu

Simple config file generation library. Glu refers to *glue*ing variables and templates.

Glu is simple python library to make your config configurable. Sometimes config files are largely 
duplicated, differ a little. You can apply DRY principle for that. You might use a template engines
like Jinja, or make a simple code for configuring. But Jinja template is not optimized for configuration,
and writing extra code makes you tired.
 
And Glu appeared from lack and the need of configuration-optimized template engine. Glu uses
template syntax that is similar to Jinja, but provides much robust syntax for configuration hierarchy.
With Glu, you can keep your any kind of config files DRY

## Quick Start

You need context, or `Scope` to generate template file with variables. Glu provides `Scope` object
so that you can load scope and inject variables using scope. Simple usage is:

```
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

// will be
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

// will be
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

scope.glue('{{ midterm_score.math }}')  // will be 93

```

You can specify fallback value using `??`, which will be used when former variable is undefined

``` python
scope.load({
    'score': {
        'math': 93
    }
})

scope.glue('{{ score.science ?? score.history ?? score.math }}')  // will be 93
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

// will be
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

```
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

// will be an empty dict
{}
```

And last, you can insert temporal scope for resolving expression, which enables to
use template as a function. This scope injection is the key feature of Glu.

```
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

// will be
{
    'hello_foo': 'hello, foo',
    'hello_bar': 'hello, bar'
}
```