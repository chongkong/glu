# Glu
------

Simple config file generation library. Glu refers to __glue__ing variables and templates.

Sometimes config files are largely duplicated, differ a little. You can apply DRY principle for that. You might use a
template engines like Jinja, or make a simple code for configuring. Glu is simple python library to make your config
configurable.

## Quick Start

It's syntax similar to other template engines.

``` json
{
    "name": "World"
}

{
    "greeting": "Hello, {{ name }}"
}

// generated
{
    "greeting": "Hello, World"
}
```

If template expression is used solely (not interpolated), its value is inserted, whatever value type is.
Also you can access nested scope using `.`

``` json

{
    "counting": {
        "number": [1, 2, 3],
        "english": ["one", "two", "three"]
    }
}

{
    "123": "{{counting.number}}"
    "one_two_three": "{{counting.english}}"
}

// generated
{
    "123": [1, 2, 3]
    "one_two_three": ["one", "two", "three"]
}

```


