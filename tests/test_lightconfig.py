#coding=utf-8
from __future__ import unicode_literals
import os
import sys
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

from lightconfig import LightConfig


def test_read_write_by_attr():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1.english = 'hello'
        cfg.section2.chinese = '你好'
        cfg.section3.japanese = 'こんにちは'
        # read
        cfg = LightConfig('tmp.ini')
        assert cfg.section1.english == 'hello'
        assert cfg.section2.chinese == '你好'
        assert cfg.section3.japanese == 'こんにちは'
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
            
            
def test_read_write_by_item():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg['section1']['english'] = 'hello'
        cfg['section2']['chinese'] = '你好'
        cfg['section3']['japanese'] = 'こんにちは'
        # read
        cfg = LightConfig('tmp.ini')
        assert cfg['section1']['english'] == 'hello'
        assert cfg['section2']['chinese'] == '你好'
        assert cfg['section3']['japanese'] == 'こんにちは'
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        

def test_delete_by_attr():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1.english = 'hello'
        cfg.section2.chinese = '你好'
        # delete
        del cfg.section1.english
        del cfg.section2
        cfg = LightConfig('tmp.ini')
        assert 'english' not in cfg.section1
        assert 'section2' not in cfg
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        
        
def test_delete_by_item():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg['section1']['english'] = 'hello'
        cfg['section2']['chinese'] = '你好'
        # delete
        del cfg['section1']['english']
        del cfg['section2']
        cfg = LightConfig('tmp.ini')
        assert 'english' not in cfg['section1']
        assert 'section2' not in cfg
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        

def test_dictable():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1.english = 'hello'
        cfg.section2.chinese = '你好'
        # convert cfg to dict
        cfg = LightConfig('tmp.ini')
        dict_cfg = dict(cfg)
        assert 'section1' in dict_cfg
        assert dict_cfg['section2']['chinese'] == '你好'
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')


def test_section_dictable():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1.english = 'hello'
        # convert cfg to dict
        cfg = LightConfig('tmp.ini')
        dict_section1 = dict(cfg.section1)
        assert 'english' in dict_section1
        assert dict_section1['english'] == 'hello'
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')


def test_update_by_section():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1 = {'option1': 'value1', 'option2': 'value2'}
        cfg['section2'] = {'option1': 'value1', 'option2': 'value2'}
        # read
        cfg = LightConfig('tmp.ini')
        assert cfg.section1.option1 == 'value1'
        assert cfg.section1.option2 == 'value2'
        assert cfg['section2']['option1'] == 'value1'
        assert cfg['section2']['option2'] == 'value2'
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')

        
def test_iterable():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1 = {'option1': 'value1', 'option2': 'value2'}
        cfg['section2'] = {'option1': 'value1', 'option2': 'value2'}
        # read
        cfg = LightConfig('tmp.ini')
        for section_k, section_v in cfg:
            print(section_k, section_v)
            for option_k, option_v in section_v:
                assert cfg[section_k][option_k] == option_v
    finally:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
    