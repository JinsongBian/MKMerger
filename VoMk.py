#!/usr/bin/python

from __future__ import print_function
import argparse
import sys,os
import re

class VoMK:
    '''this class is used to merge Android make files.
       first add several Android.mk files, then generate a merged one.'''
    def __init__(self):
        self.src_files = []
        self.libraries = []
        self.includes = []

    def add_mk(self, mkpath):
        '''add and parse a mk file, extract src file list and libraries'''
        mkroot=""
        pairs = {'LOCAL_SRC_FILES':'','LOCAL_LDLIBS':'',
                 'LOCAL_C_INCLUDES':''}

        def parse():
            fp = open(mkpath)
            while True:
                line = fp.readline()
                if not line: break
                _line = line.strip()
                _pos = _line.find(':=')
                if _pos > 0:
                    _token = _line[:_pos].strip()
                    _value = _line[_pos+2:].strip()
                    while _value[-1]=='\\':
                        _value = _value[:-1].strip()
                        _line = fp.readline()
                        if not _line: break
                        _value = _value + ' ' + _line.strip()
                    pairs[_token] = _value
            fp.close()

        def process():
            _files = pairs['LOCAL_SRC_FILES'].split()
            for _file in _files:
                if _file.find('$(')>=0:
                    _var = _file[_file.find('$(')+2:_file.find(')')]
                    _relpath = os.path.join(mkroot,
                                    _file.replace("$("+_var+")", pairs[_var]))
                else:
                    _relpath = os.path.join(mkroot,_file)
                _abspath = os.path.abspath(_relpath)
                if not _abspath in self.src_files:
                    self.src_files.append(_abspath)
                    
            _incs = pairs['LOCAL_C_INCLUDES'].split()
            for _inc in _incs:
                if _inc.find('$(')>=0:
                    _var = _inc[_inc.find('$(')+2:_inc.find(')')]
                    _relpath = os.path.join(mkroot,
                                    _inc.replace("$("+_var+")", pairs[_var]))
                else:
                    _relpath = os.path.join(mkroot,_inc)
                _abspath = os.path.abspath(_relpath)
                if not _abspath in self.includes:
                    self.includes.append(_abspath)
                    
            _libs = pairs['LOCAL_LDLIBS'].split()
            for _lib in _libs:
                if not _lib.endswith('.a'): continue
                if _lib.find('$(')>=0:
                    _var = _lib[_lib.find('$(')+2:_lib.find(')')]
                    _relpath = os.path.join(mkroot,
                                    _lib.replace("$("+_var+")", pairs[_var]))
                else:
                    _relpath = os.path.join(mkroot,_lib)
                _abspath = os.path.abspath(_relpath)
                if not _abspath in self.libraries:
                    self.libraries.append(_abspath)
                   
        if os.path.exists(mkpath):
            mkroot = os.path.dirname(mkpath)
            parse()
            process()

    def generate(self, out_path="./Android.mk"):
        '''generate a Android.mk with merged src files and libraries'''
        pass

    def printing(self):
        print("Src Files:")
        for item in self.src_files:
            print(item)
        print("Includes:")
        for item in self.includes:
            print(item)
        print("Libraries:")
        for item in self.libraries:
            print(item)



def main():
    testp = "/cygdrive/d/_Works/main/Source/PushPD/Project/Linux/ndk/jni/Android.mk"
    voMK = VoMK()
    voMK.add_mk(testp)
    t2 = "/cygdrive/d/_Works/main/Codec/Audio/DTS/ndk/v6/jni/Android.mk"
    voMK.add_mk(t2)
    t3 = "/cygdrive/d/_Works/main/Utility/voVersion/prj/linux/ndk/v7/jni/Android.mk"
    voMK.add_mk(t3)
    voMK.printing()

if __name__ == "__main__":
  main()
