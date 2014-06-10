#!/usr/bin/python

from __future__ import print_function
import argparse
import xml.etree.ElementTree as ET
import sys,os           

OSORDER = {
    'a':0,
    'a7':1,
    'ax86':10,
    'i':4,
    'i386':5,
    'w':6,
    'tc':2,
    'tc7':3,
    'ax86tc':11,
    'w64':12,
    'i86':8,
    'i64':9
    }
def get_project_path(module, OSType, SVNRoot='/'):
    '''get project path for specified module and OS'''
    if SVNRoot=='/':
        SVNRoot = os.getenv("WB_SRC_DIR")

    cfg_path = os.path.join(SVNRoot, 'build',
                            'config','lib-config.xml')
    if (not (os.path.exists(cfg_path))):
        return ""

    libcfg = ET.parse(cfg_path)
    cfgroot = libcfg.getroot()

    _module = os.path.basename(module)
    _module = os.path.splitext(_module)[0]
    if _module.startswith("libvo"):
        _module=_module[3:]

    items = cfgroot.findall("./node[file='"+ _module +"']/make/item")

    if len(items)>OSORDER[OSType]:
        path = items[OSORDER[OSType]].text
        if len(path)>8:
            return(path)
    return ""

def main():
    '''This tool is called by autobuild, copy modules per defined rule'''
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-src', dest='SVNRoot',
                         default=os.getenv("WB_SRC_DIR"),
                         help='SVN root path')
    _parser.add_argument('-os', dest='os', default='a',
                         choices=['a','i','i386','w','a7','ax86',
                                  'tc','tc7','ax86tc','w64','i86','i64'],
                         help='Operation system type.')
    _parser.add_argument('module',
                         help='an module name')
    _args = _parser.parse_args()

######debugging####
    if not _args.SVNRoot:
        _args.SVNRoot = "/cygdrive/d/linux/voCode/Onelib"
    if not _args.os:
        _args.os = "a"
    #print(_args)
###################
    path = get_project_path(_args.module, _args.os, SVNRoot=_args.SVNRoot)
    if len(path)>8:
        print(path)
 
if __name__ == "__main__":
  main()
