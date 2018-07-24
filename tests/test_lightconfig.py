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
        print(cfg)
        cfg = LightConfig('tmp.ini')
        assert cfg.section1.english == 'hello'
        assert cfg.section2.chinese == '你好'
        assert cfg.section3.japanese == 'こんにちは'
    except:
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
        print(cfg)
        cfg = LightConfig('tmp.ini')
        assert cfg['section1']['english'] == 'hello'
        assert cfg['section2']['chinese'] == '你好'
        assert cfg['section3']['japanese'] == 'こんにちは'
    except:
        if os.path.exists('tmp.ini'):
            os.remove('tmp.ini')
