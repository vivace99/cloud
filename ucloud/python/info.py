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
    lb_list = CallAPI('lb', 'listLoadBalancers', None, 'loadbalancer', [{'field':'name', 'search':'dt-kakao-https2'}], None, None, False)
    ClearScreen()
    '''
    for index_lb, lb in enumerate(lb_list):
        svm_list = CallAPI('lb', 'listLoadBalancerWebServers', {'loadbalancerid':lb['loadbalancerid']}, 'loadbalancerwebserver', None, None, None, False)
        for index_svm, svm in enumerate(svm_list):
            #print 'remove lb_webserver ' + svm['ipaddress'] + ' -> ' + svm['publicport'] + ' from ' + lb['name']
            resp_removelb = CallAPI('lb', 'removeLoadBalancerWebServer', {'serviceid':svm['serviceid']}, None, None, None, None, False)
            print resp_removelb'''