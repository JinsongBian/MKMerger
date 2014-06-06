#!/usr/bin/python

from __future__ import print_function
import argparse
import sys,os  

class VoMK:
    '''this class is used to merge Android make files.
       first add several Android.mk files, then generate a merged one.'''
    def __init__(self):
        self.src_files = []
        self.libraries = []

    def add_mk(self, mkpath):
        '''add and parse a mk file, extract src file list and libraries'''
        pass

    def generate(self, out_path="./Android.mk"):
        '''generate a Android.mk with merged src files and libraries'''
        pass
