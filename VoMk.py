#!/usr/bin/python

from __future__ import print_function
import argparse
import sys,os
import re
from getproject_path import get_project_path

TKSRCFILES = 'LOCAL_SRC_FILES'
TKLIBS = 'LOCAL_LDLIBS'
TKINCLUDES = 'LOCAL_C_INCLUDES'
TKSR = 'SRCROOT'
TKGOON = ' \\\n'

class VoMK:
    '''this class is used to merge Android make files.
       first add several Android.mk files, then generate a merged one.'''

    def __init__(self):
        self.src_files = []
        self.libraries = []
        self.includes = []
        self.SVNRoot = ''

    def add_mk(self, mkpath):
        '''add and parse a mk file, extract src file list and libraries'''
        mkroot=""
        pairs = {TKSRCFILES:'', TKLIBS:'',
                 TKINCLUDES:''}

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
            _files = pairs[TKSRCFILES].split()
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
                if _abspath.endswith('/Common/voLog.c'):
                    self.SVNRoot = _abspath[:_abspath.find('/Common/voLog.c')] 
                    
            _incs = pairs[TKINCLUDES].split()
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
                    
            _libs = pairs[TKLIBS].split()
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

    def remove_svn_root(self):
        _sr = self.SVNRoot+os.sep
        _len = len(self.SVNRoot)+1
        if _len < 2:
            return
        for _idx in range(0, len(self.src_files)):
            if self.src_files[_idx].startswith(_sr):
                self.src_files[_idx] = self.src_files[_idx][_len:]
        for _idx in range(0, len(self.includes)):
            if self.includes[_idx].startswith(_sr):
                self.includes[_idx] = self.includes[_idx][_len:]
        for _idx in range(0, len(self.libraries)):
            if self.libraries[_idx].startswith(_sr):
                self.libraries[_idx] = self.libraries[_idx][_len:]

    def render(self):
        _head = '''
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_ARM_MODE := arm

LOCAL_MODULE := libvoOnelib

'''
        _root = TKSR + ' := ' + self.SVNRoot +'\n\n'
        _ref = '$('+ TKSR +')' + os.sep

        _srcfiles = TKSRCFILES + ' :=' + TKGOON
        for _item in self.src_files:
            _srcfiles += '\t\t' + _ref + _item + TKGOON
        _srcfiles += '\n'
            
        _incs = TKINCLUDES + ' :=' + TKGOON
        for _item in self.includes:
            _incs += '\t\t' + _ref + _item + TKGOON
        _incs += '\n'

        _mid = '''
VOMM := -D__arm -D__VO_NDK__ -DLINUX -D_LINUX -D_LINUX_ANDROID -D_VOLOG_ERROR -D_VOLOG_INFO -D_VOLOG_WARNING

# about info option, do not need to care it
LOCAL_CFLAGS := -D_VOMODULEID=0x0a310000  -DNDEBUG -DARM -DARM_ASM -march=armv6j -mtune=arm1136jf-s -mfpu=vfp  -mfloat-abi=softfp -msoft-float -fsigned-char 

'''
        _libs = TKLIBS + ' := -llog -lvodl -L' + _ref + 'Lib/ndk ' + TKGOON
        for _item in self.libraries:
            _libs += '\t\t' + _ref + _item + TKGOON
        _libs += '\n'
        
        _end = '''
include $(SRCROOT)/build/vondk.mk
include $(BUILD_SHARED_LIBRARY)
'''
        return _head + _root + _srcfiles + _incs + _mid + _libs + _end

        
    def generate(self, out_path="./Android.mk"):
        '''generate a Android.mk with merged src files and libraries'''
        pass

    def printing(self):
        print("SVNRoot:\n",self.SVNRoot)
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
    tr = "/cygdrive/d/linux/voCode/main"
    if not os.path.exists(tr):
        tr = "/cygdrive/d/_Works/main"
    t1 = tr + "/Source/PushPD/Project/Linux/ndk/jni/Android.mk"
    t2 = tr + "/Codec/Audio/DTS/ndk/v6/jni/Android.mk"
    t3 = tr + "/Utility/voVersion/prj/linux/ndk/v7/jni/Android.mk"
    voMK = VoMK()
    voMK.add_mk(t1)
    #voMK.printing()
    #print()
    voMK.add_mk(t2)
    #voMK.printing()
    #print()
    voMK.add_mk(t3)
    #voMK.printing()
    voMK.remove_svn_root()
    print(voMK.render())
#    voMK.printing()
    

if __name__ == "__main__":
  main()
