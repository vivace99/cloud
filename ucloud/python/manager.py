# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

import sys
import getopt
import getpass
from was import WAS
from info import INFO
from base import *

UCLOUD_API_KEY = 'XJgePBKStnGIVB5MwNnsRx9a-WsUNAWgOLsudCMOsgCvkKqyAsViM4Jxr-aZgvt6UfpB74Jgbj2XES0zbQ3kng'
UCLOUD_SECRET  = 'uGBRE4pFXUGhnjaz-x1HDKefJAP1m6KKVXTM-mJXWr0K78VtySzFN4Nn9XNPjKqqB7GVI_gEY1lYoN3qEWY-CA'

class UCLOUD(Base):
    def __init__(self, _api_key, _secret):
        Base.__init__(self, _api_key, _secret)
        self.menus = ['INFO', 'WAS', 'Exit']
        self.jobid = []
    
    def RunMenu(self, _choice):
        if _choice == 1:
            info = INFO(self.api_key, self.secret)
            info.Run()
        elif _choice == 2:
            was = WAS(self.api_key, self.secret)
            was.Run()

def main():
    manager = UCLOUD(UCLOUD_API_KEY, UCLOUD_SECRET)
    manager.Run()

if __name__ == '__main__':
  main()