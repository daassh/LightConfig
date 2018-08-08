#!/usr/bin/env python
# coding=utf-8
# get a easy way to edit config file
"""
>>> from lightconfig import LightConfig
>>> cfg = LightConfig("config.ini")
>>> cfg.section1.option1 = "value1"
>>> print(cfg.section1.option1)
value1
>>> "section1" in cfg
True
>>> "option1" in cfg.section1
True
"""
import os
import codecs
import locale
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


class ConfigParserOptionCaseSensitive(ConfigParser):
    """
    add case sensitve to ConfigParser
    """
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults)
    def optionxform(self, option_str):
        return option_str


class LightConfig(object):
    def __init__(self, config_path, try_encoding={'utf-8', 'utf-8-sig', locale.getpreferredencoding().lower()}, try_convert_digit = False):
        self.__dict__['_config_path'] = config_path
        self.__dict__['_try_encoding'] = try_encoding if isinstance(try_encoding, (list, tuple, set)) else [try_encoding]
        self.__dict__['_try_convert_digit'] = try_convert_digit
        self.__dict__['_config'] = ConfigParserOptionCaseSensitive()
        if not os.path.exists(config_path):
            dir_path = os.path.dirname(os.path.abspath(config_path))
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            open(config_path, 'a').close()
        LightConfig._read(self)
        self.__dict__['_cached_stamp'] = LightConfig._stamp(self)
    
    def __str__(self):
        return str(LightConfig._as_dict(self))

    def __repr__(self):
        return repr(LightConfig._as_dict(self))

    def __iter__(self):
        return iter(LightConfig._as_dict(self).items())

    def __getattribute__(self, item):
        if item in ('keys', '__dict__'):
            return super(LightConfig, self).__getattribute__(item)
        else:
            return LightConfig.__getattr__(self, item)

    def __getattr__(self, item):
        return LightConfig.Section(self, item, self.__dict__['_try_convert_digit'])

    __getitem__ = __getattr__

    def __setattr__(self, name, value):
        try:
            value = dict(value)
        except:
            raise ValueError('"{}" is not dictable'.format(value))
        else:
            LightConfig.__dict__['__delattr__'](self, name)
            section = LightConfig.Section(self, name, self.__dict__['_try_convert_digit'])
            for k, v in value.items():
                LightConfig.Section.__setattr__(section, k, v)

    __setitem__ = __setattr__

    def __delattr__(self, item):
        if item in self:
            self.__dict__['_config'].remove_section(item)
            LightConfig._save(self)
    
    __delitem__ = __delattr__
   
    def __contains__(self, item):
        return self.__dict__['_config'].has_section(item)
        
    def _as_dict(self):
        res = {}
        for section in self.keys():
            res[section] = self[section]
        return res

    def keys(self):
        return self.__dict__['_config'].sections()

    def _read(self):
        for encoding in self.__dict__['_try_encoding']:
            fp = codecs.open(self.__dict__['_config_path'], encoding=encoding)
            try:
                self.__dict__['_config'].readfp(fp)
            except:
                err = True
            else:
                err = False
                self.__dict__['_encoding'] = encoding
                break
        if err:
            raise UnicodeError("\"{}\" codec can't decode this config file".format(', '.join(self.__dict__['_try_encoding'])))
        
    def _save(self):
        self.__dict__['_config'].write(codecs.open(self.__dict__['_config_path'], "w", encoding=self.__dict__['_encoding']))
        self.__dict__['_cached_stamp'] = LightConfig._stamp(self)

    def _stamp(self):
        return os.stat(self.__dict__['_config_path']).st_mtime
        
    class Section(object):
        def __init__(self, conf, section, try_convert_digit):
            self.__dict__['_section'] = section
            self.__dict__['_conf'] = conf
            self.__dict__['_try_convert_digit'] = try_convert_digit

        def __str__(self):
            return str(LightConfig.Section._as_dict(self))

        def __repr__(self):
            return repr(LightConfig.Section._as_dict(self))
        
        def __iter__(self):
            return iter(LightConfig.Section._as_dict(self).items())

        def __getattribute__(self, item):
            if item in ('keys', '__dict__'):
                return super(LightConfig.Section, self).__getattribute__(item)
            else:
                return LightConfig.Section.__getattr__(self, item)

        def __getattr__(self, option):
            current_stamp = LightConfig._stamp(self.__dict__['_conf'])
            if current_stamp != self.__dict__['_conf'].__dict__['_cached_stamp']:
                LightConfig._read(self.__dict__['_conf'])
                self.__dict__['_conf'].__dict__['_cached_stamp'] = current_stamp
            value = self.__dict__['_conf'].__dict__['_config'].get(self.__dict__['_section'], option)
            if self.__dict__['_try_convert_digit']:
                try:
                    value = eval(value)
                except:
                    pass
            return value

        __getitem__ = __getattr__
        
        def __setattr__(self, key, value):
            if not self.__dict__['_section'] in self.__dict__['_conf']:
                self.__dict__['_conf'].__dict__['_config'].add_section(self.__dict__['_section'])
            self.__dict__['_conf'].__dict__['_config'].set(self.__dict__['_section'], key, str(value))
            LightConfig._save(self.__dict__['_conf'])

        __setitem__ = __setattr__
        
        def __delattr__(self, item):
            if item in self:
                self.__dict__['_conf'].__dict__['_config'].remove_option(self.__dict__['_section'], item)
                LightConfig._save(self.__dict__['_conf'])
            
        __delitem__ = __delattr__
                
        def __contains__(self, item):
            return self.__dict__['_conf'].__dict__['_config'].has_option(self.__dict__['_section'], item)
            
        def _as_dict(self):
            return dict(self.__dict__['_conf'].__dict__['_config'].items(self.__dict__['_section']))
            
        def keys(self):
            return self.__dict__['_conf'].__dict__['_config'].options(self.__dict__['_section'])
