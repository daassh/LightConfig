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


class LightConfig:
    def __init__(self, config_path, try_encoding={'utf-8', 'utf-8-sig', locale.getpreferredencoding().lower()}, try_convert_digit = True):
        self._config_path = config_path
        self._try_encoding = try_encoding if isinstance(try_encoding, (list, tuple, set)) else [try_encoding]
        self._try_convert_digit = try_convert_digit
        self._config = ConfigParserOptionCaseSensitive()
        if not os.path.exists(config_path):
            dir_path = os.path.dirname(os.path.abspath(config_path))
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            open(config_path, 'a').close()
        self._read()
        self._cached_stamp = self._stamp()
    
    def __str__(self):
        return str(self.as_dict())

    def __repr__(self):
        return repr(self.as_dict())

    def __iter__(self):
        return iter(self._config.sections())

    def __getattr__(self, item):
        return self.Section(self, item, self._try_convert_digit)

    __getitem__ = __getattr__
        
    def __delattr__(self, item):
        self._config.remove_section(item)
        
    __delitem__ = __delattr__
        
    def __contains__(self, item):
        return self._config.has_section(item)
        
    def as_dict(self):
        res = {}
        for section in self._config.sections():
            res[section] = dict(self._config.items(section))
        return res

    def sections(self):
        return self._config.sections()
        
    def _read(self):
        for encoding in self._try_encoding:
            fp = codecs.open(self._config_path, encoding=encoding)
            try:
                self._config.readfp(fp)
            except Exception as e:
                err = True
            else:
                err = False
                self._encoding = encoding
                break
        if err:
            raise UnicodeError("\"{}\" codec can't decode this config file".format(', '.join(self._try_encoding)))
        
    def _save(self):
        self._config.write(codecs.open(self._config_path, "w", encoding=self._encoding))
        self._cached_stamp = self._stamp()

    def _stamp(self):
        return os.stat(self._config_path).st_mtime
        
    class Section:
        def __init__(self, conf, section, try_convert_digit):
            self._section = section
            self._conf = conf
            self._try_convert_digit = try_convert_digit

        def __str__(self):
            return str(self.as_dict())

        def __repr__(self):
            return repr(self.as_dict())
            
        def __iter__(self):
            return iter(self._conf._config.options(self._section))

        def __getattr__(self, option):
            current_stamp = self._conf._stamp()
            if current_stamp != self._conf._cached_stamp:
                self._conf._read()
                self._conf._cached_stamp = current_stamp
            value = self._conf._config.get(self._section, option)
            if self._try_convert_digit:
                try:
                    value = eval(value)
                except:
                    pass
            return value

        __getitem__ = __getattr__
            
        def __setattr__(self, key, value):
            if key not in ("_section", "_conf", "_try_convert_digit"):
                if not self._conf._config.has_section(self._section): 
                    self._conf._config.add_section(self._section)
                self._conf._config.set(self._section, key, str(value))
                self._conf._save()
            else:
                self.__dict__[key] = value

        __setitem__ = __setattr__
        
        def __delattr__(self, item):
            self._conf._config.remove_option(self._section, item)
            
        __delitem__ = __delattr__
                
        def __contains__(self, item):
            return self._conf._config.has_option(self._section, item)
                
        def as_dict(self):
            return dict(self._conf._config.items(self._section))
            
        def options(self):
            return self._conf._config.options(self._section)
        