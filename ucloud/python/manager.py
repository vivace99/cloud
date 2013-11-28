# -*- coding: utf-8 -*-
# pip install ucloud
__author__ = 'Edward Lee'

import sys
import getopt
import getpass
from was import WAS
from info import INFO
from base import *

class UCLOUD(Base):
    def __init__(self):
        Base.__init__(self)
        self.menus = ['INFO', 'WAS', 'Exit']
        self.jobid = []
    
    def RunMenu(self, _choice):
        if _choice == 1:
            info = INFO()
            info.Run()
        elif _choice == 2:
            was = WAS()
            was.Run()

def main():
    manager = UCLOUD()
    manager.Run()

if __name__ == '__main__':
  main()