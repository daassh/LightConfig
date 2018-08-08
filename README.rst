LightConfig
===========

The LightConfig library enables you to get a easy way to create or read config file

Installation
------------

LightConfig is conveniently available via pip:

::

    pip install lightconfig
    
or installable via ``git clone`` and ``setup.py``

::

    git clone https://github.com/daassh/LightConfig.git
    python setup.py install
    
Usage
-----
Import
>>>>>>

.. code:: python

    from lightconfig import LightConfig

Create
>>>>>>

.. code:: python

    cfg = LightConfig("config.ini")

`(if specific path not exists, the path file will be create)`

Read / Write
>>>>>>>>>>>>
Usually, you can read/write config by both attribute and item

read/write by attribute
:::::::::::::::::::::::
.. code:: python

    >>> cfg.section.option = 'value'
    >>> cfg.section.option
    'value'

read/write by item
::::::::::::::::::
.. code:: python

    >>> cfg['section']['option'] = 'value'
    >>> cfg['section']['option']
    'value'

write by section
::::::::::::::::
.. code:: python

   >>> cfg.section1 = {'option1': 'value1'}
   >>> cfg['section2'] = {'option2': 'value2'}
   >>> cfg
   {'section1': {'option1': 'value1'}, 'section2': {'option2': 'value2'}}

But in some situation, you can only use `read/write by item`:

section/option name can't be python variable name
:::::::::::::::::::::::::::::::::::::::::::::::::
wrong

.. code:: python

    >>> cfg.section-2.2option = 'value2'
      ...
    SyntaxError: invalid syntax

right

.. code:: python

    >>> cfg['section-2']['2option'] = 'value2'

section/option name is `keys` or `__dict__`
:::::::::::::::::::::::::::::::::::::::::::

`keys` and `__dict__` are inner method of `LightConfig` (`keys` used to make `LightConfig` object dictable, `__dict__` used to visit other inner method of `LightConfig`), so when using `keys` or `__dict__` as section/option name, you can only access it by item:

wrong

.. code:: python

   >>> cfg.keys.option3 = 'value3'
     ...
   AttributeError: 'method' object has no attribute 'option3
   >>> cfg.keys
   <bound method LightConfig.keys of ...>
   >>> cfg.__dict__.option4 = 'value4'
     ...
   AttributeError: 'dict' object has no attribute 'option4'
   >>> cfg.__dict__
   {'_config_path': '', '_try_encoding': {}, ...}

right

.. code:: python

   >>> cfg['keys'].option3 = 'value3'
   >>> cfg['keys']
   {'option3': 'value3'}
   >>> cfg['__dict__'].option4 = 'value4'
   >>> cfg['__dict__']
   {'option4': 'value4'}

Delete
>>>>>>
use `del` to delete section/option:

.. code:: python

    >>> del cfg.section.option
    >>> 'option' in cfg.section
    False
    >>> del cfg['section']
    >>> 'section' in cfg
    False

Dictable
>>>>>>>>
use `dict` to convert `LightConfig` or `LightConfig.Section` object to dict:

.. code:: python

    >>> type(dict(cfg))
    <class 'dict'>
    >>> type(dict(cfg.section))
    <class 'dict'>

Iterable
>>>>>>>>

.. code:: python

   >>> for section_name, section_info in cfg:
   ...     print(section_name)
   ...     for option, value in section_info:
   ...         print('  {}={}'.format(option, value))
   section1
     option1=value1
   section2
     option2=value2
