# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

from base import *

class INFO(Base):
    def __init__(self, _api_key, _secret):
        Base.__init__(self, _api_key, _secret)
        self.menus = ['server list', 'zone list', 'product list', 'snapshot list', 'template list', 'volume list', 'main']
    
    def RunMenu(self, _choice):
        if _choice == 1:
            ServerList(self.api_key, self.secret)
        elif _choice == 2:
            ZoneList(self.api_key, self.secret)
        elif _choice == 3:
            ProductList(self.api_key, self.secret)
        elif _choice == 4:
            SnapshotList(self.api_key, self.secret)
        elif _choice == 5:
            TemplateList(self.api_key, self.secret)
        elif _choice == 6:
            VolumeList(self.api_key, self.secret)