Holtzman
========

Holtzman is a simple templating engine for Python.

Installation
------------

Holtzman can be installed using pip

   pip install holtzman

Usage
-----

The main `Template` class is imported from `holtzman.template`.  The constructor excepts a `Stream` object that supports a `read` method.

The `Template.from_string` and `Template.from_file` static methods will compile a template from a string and a file name respectively.

Examples:
::
    from holtzman.template import Template

    string_template = Template.from_string('hello world')

    file_template = Template.from_file('template.hz')

A compiled template can then be rendered by calling the render method and passing in the required variables, e.g.
:: 
   string_template.render({ 'variable': 'hello_world' })

The variables parameter can be a dict or object.  If it's a dict the variable names in the template will be used as keys for the dict to find the required values, if an object is passed then holtzman will look for properties that match the variable names in the template.  Any combination of dicts and objects may be used in nested variables.


Templates
~~~~~~~~~

Templates support variable substituion, conditions and for loops.

Variable Substitution
^^^^^^^^^^^^^^^^^^^^^

Variables can be embedded in templates using the following format:
::
   {{ variable_name }}

Nested variables can be embedded:
::
   {{ parent.child }}

If conditions
^^^^^^^^^^^^^

If conditions are used as follows:
::
   {% if variable %}
      this is rendered if variable is true
   {% end %}

For loops
^^^^^^^^^

For loops work as follows:
::
   {% for variable in list %}
      {{ variable }}
   {% end %}

For loops and if conditions can be nested arbitrarily, e.g:
::
   {% for parent in parent_list %}
      {% for child in child_list %}
         {{ parent }} : {{ child }}
      {% end %}
   {% end %}
