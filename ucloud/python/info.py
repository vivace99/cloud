# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

from base import *

class INFO(Base):
    def __init__(self):
        Base.__init__(self)
        self.menus = ['server list', 'zone list', 'product list', 'snapshot list', 'template list', 'volume list', 'network list', 'ip list', 'firewall list', 'port forward list', 'load balancer list', 'test', 'main']
    
    def RunMenu(self, _choice):
        if _choice == 1:
            ServerList()
        elif _choice == 2:
            ZoneList()
        elif _choice == 3:
            ProductList()
        elif _choice == 4:
            SnapshotList()
        elif _choice == 5:
            TemplateList()
        elif _choice == 6:
            VolumeList()
        elif _choice == 7:
            NetworkList()
        elif _choice == 8:
            AddressList()
        elif _choice == 9:
            FireWallList()
        elif _choice == 10:
            PortForwardList()
        elif _choice == 11:
            LoadBalancerList()
        elif _choice == 12:
            Test({'id':'test', 'displayname':'dt-kakao-was-p1-node1'})



########## 테스트 함수 ##########
def Test(result):
    if '-was-' in result['displayname']:
        # new WAS VM
        node_id = result['id']
        node_name = result['displayname']
        node_nas = int(node_name[14:node_name.index('-node')])
        node_number = int(node_name[node_name.index('-node')+5])
        # get used port for service
        api_type = 'server'
        command = 'listPortForwardingRules'
        data_param = None
        node_name = 'portforwardingrule'
        data_filter = [{'field':'ipaddress', 'search':'14.63.170.144'}]
        result = None
        param = None
        port_used = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, False)
        port_http = 80
        port_https = 443
        port_http_map = {}
        port_https_map = {}
        for index, row in enumerate(port_used):
            if int(row['publicport']) < 443:
                port_http_map[row['publicport']] = 'O'
            else:
                port_https_map[row['publicport']] = 'O'
        while str(port_http) in port_http_map:
            port_http += 1
        while str(port_https) in port_https_map:
            port_https += 1
        print 'use ' + str(port_http) + ' and ' + str(port_https)