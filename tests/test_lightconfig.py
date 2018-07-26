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
    except:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        raise
            
            
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
    except:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        raise
        

def test_delete_by_attr():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg.section1.english = 'hello'
        cfg.section2.chinese = '你好'
        # delete
        del cfg.section1.english
        assert 'english' not in cfg.section1
        del cfg.section2
        assert 'section2' not in cfg
    except:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        raise
        
        
def test_delete_by_item():
    try:
        # write
        cfg = LightConfig('tmp.ini')
        cfg['section1']['english'] = 'hello'
        cfg['section2']['chinese'] = '你好'
        # delete
        del cfg['section1']['english']
        assert 'english' not in cfg['section1']
        del cfg['section2']
        assert 'section2' not in cfg
    except:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
        raise
        