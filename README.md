[![Build Status](https://travis-ci.org/yogevyuval/confit.svg?branch=master)](https://travis-ci.org/yogevyuval/confit)

# Overview
Generate template based configuration files from centralized KV stores like aws SSM.

# Usage
```
confit --region us-east-1 -i config.jinja -o output.yaml
```

# Template
`confit` uses the [jinja2](http://jinja.pocoo.org/docs/2.10/) templating language.

ֿParameters are available in the template through the `vars` variable.

You can use `{{ vars.get('/parameter/param1/') }}`, or `{{ vars.get('/parameter/param1/' }}, 'default')` to have a default.
Access through `{{ vars['/parameter/param1/'] }} ` is also supported. 


# Prefix
If you supply a `prefix` option, every option that starts with this prefix will be available through `prefixed_vars` in the same API as `vars`.

For example
if you have the following parameters: `/production/some/param1`, `/production/some/param2` and you you provide `--prefix /production` you can access the params like so:
`prefixed_vars.get('/some/param1')`

# Options
* `--region` (string) - The region to connect to
* `--prefix` (string) - The prefix to use to generate `prefixed_vars`
* `--input-template / -i` (string) - The path to the input template
* `--output / -o` (string) - If supplied, the output will be written to the output file


