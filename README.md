# Glu

Glu is a simple config file generation command line tool. Glu refers to 
*glue*ing variable scopes to template, using only JSON or YAML file. 
This makes your configuration configurable as much DRY as you can.

Its syntax is similar to those of other template engines, like Jinja,
but it is more like a programming using JSON or YAML. Glu provides much
robust syntax for generating configuration, and highly optimized for
only generating configurations.

## How to install?

Support any python version. If you are having an compatibility issue,
please let me know.

```
$ pip install glu
```

If you want to install it globally, add `sudo` in front of the command.

## Quick Start

You need to provide ***source*** files, which would be used as a variable
scope, and a ***template*** file, to which variables of scope will be
injected, or _glued_.

If your source files and template file is ready, just run:


``` shell
$ glu -s source_file [source_file...] -t template_file -o output_file [-e]
```

For example,

``` shell
$ glu -s /path/to/source_file.json\
         /path/to/yaml_source_file.yml\ 
      -t /path/to/template_file.json\
      -o /path/to/output_file.json\
      -e  # if you want to use environment variable
```

### Grammar Basics

Rules for gluing is basically substitution. Variable from source file
is registered as a ***global*** scope, and can be used in any places.

``` json
# source
{
  "name": "¯\\_(ツ)_/¯"
}

# template
{
  "greeting": "Hello, {{ name }}"
}

# generated
{
  "greeting": "Hello, ¯\\_(ツ)_/¯"
}
```

You can substitute variables of arbitrary type, and if variable is
within the string, it will be interpolated like above. But be careful 
not to use non-string variable within the string, because it cannot be
interpolated properly. (integer is OK)

If you want to access variable in another dictionary variable, you can
use `.` for nested access. Dot (`.`) is evaluated generously, that is if 
`foo.bar` will be evaluated to ***undefined*** if `foo` is 
***undefined*** or `foo.bar` is ***undefined***, without throwing null
reference exception. Dot will be used very frequently in your JSON code.

``` json
# scope
{
  "array": [1, 2, 3],
  "dictionary": {
    "foo": "¯\\_(ツ)_/¯",
    "bar": "{{ array }}"
  }
}

# template
{
  "result": [
    "{{ dictionary }}",
    "{{ dictionary.bar }}"
  ]
}

# generated
{
  "result": [
    {
      "foo": "¯\\_(ツ)_/¯",
      "bar": [1, 2, 3]
    },
    [1, 2, 3]
  ]
}
```

### Operators

There are some operators that makes Glu robust. Operator interface is
not stable yet, so keep in mind this operator might be changed in future,
which you have to update them manually `¯\_(ツ)_/¯`

Fallback operator looks like `??`, which uses next variable if former
variable is ***undefined***. if evaluated value is ***undefined***, Glu
will raise error.

``` python
# source
{
  "score": { "math": 93 }
)

# template
{
  "score": "{{ score.science ?? score.history ?? score.math }}"
}

# generated
{
  "score": 93
}
```

Filter operator looks like `|`, which will apply filter in rhs to value
in lhs. Let's first look at the string filters.

``` json
# source
{
  "foo": "This_isREALLYAmazing"
}

# template
{
  "display": "{{ foo | display }}",
  "camel_case": "{{ foo | camel_case }}",
  "pascal_case": "{{ foo | pascal_case }}",
  "snake_case": "{{ foo | snake_case }}",
  "lisp_case": "{{ foo | lisp_case }}",
  "uppercase": "{{ foo | uppercase }}",
  "uppercase_dash": "{{ foo | uppercase_dash }}",
  "capitalize_dash": "{{ foo | capitalize_dash }}",
}

# will be
{
    "display": "This Is Really Amazing",
    "camel_case": "thisIsReallyAmazing",
    "pascal_case": "ThisIsReallyAmazing",
    "snake_case": "this_is_really_amazing",
    "lisp_case": "this-is-really-amazing",
    "uppercase": "THIS_IS_REALLY_AMAZING",
    "uppercase_dash": "THIS-IS-REALLY-AMAZING",
    "capitalize_dash": "This-Is-Really-Amazing",
}
```

There is `mute` filter, which removes ***undefined*** fields from
dictionary or array. `mute_if_empty` field behaves the same, but removes
empty field

``` python
# source
{
    "empty_array": [],
    "empty_string": "",
    "empty_dict": {}
}

# template
{
    "foo": "{{ empty_array | mute_if_empty }}",
    "bar": "{{ empty_string | mute_if_empty }}",
    "zoo": "{{ empty_dict | mute_if_empty }}",
    "coz": "{{ undefined_variable | mute }}"
}

# generated
{}
```

Inject operator (`<`) let you inject the ***local scope*** when gluing 
variable, which will temporally override the ***global scope***.
Inject operator enables you to function-like or class-like behavior.

``` python
# source
{
  "Person": {
    "full_name": "{{ first_name }} {{ last_name }}"
  },
  "joe": {
    "first_name": "Alan",
    "last_name": "Joe"
  },
  "park": {
    "first_name": "Aiden",
    "last_name": "Park"
  }
}

# template
{
  "people": [
    "{{ Person < joe }}",
    "{{ Person < park }}"
  ]
}

# generated
{
  "people": [
    { "full_name": "Alan Joe" },
    { "full_name": "Aiden Park" }
  ]
}
```

### Predefined variables

Glu supports some variables which is useful when generating
configurations.

| Variable Name | Value |
| ----- | ----- |
| @date | Date string of format `yyyymmdd` |
| @timestamp | Integer value of unix timestamp |
| @uuid_x | Randomly issued UUID string. There are total 10 random uuid: `@uuid_0` to `@uuid_9` |
| @env | Place where environment variable is stored, if `--use-env` option is set |

Variables start with `@` are all reserved, so please do not start your
variable name with `@`.
