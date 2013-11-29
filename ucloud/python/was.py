# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

from base import *
from info import *

class WAS(Base):
    def __init__(self):
        Base.__init__(self)
        # 사용하는 존의 정보를 저장해놔서 모든 작업을 해당 존에 대해 수행
        self.zone = {'name':'KOR-Central B', 'id':'9845bd17-d438-4bde-816d-1b12f37d5080'}
        self.menus = ['add server', 'remove server', 'start server', 'stop server', 'reboot server', 'change server spec', 'main']
    
    def RunMenu(self, _choice):
        if _choice == 1:
            add = WAS_Add(self.zone)
            add.Run()
        elif _choice == 2:
            add = WAS_Remove(self.zone)
            add.Run()
        elif _choice == 3:
            add = WAS_Start(self.zone)
            add.Run()
        elif _choice == 4:
            add = WAS_Stop(self.zone)
            add.Run()
        elif _choice == 5:
            add = WAS_Reboot(self.zone)
            add.Run()
        elif _choice == 6:
            add = WAS_ChangeSpec(self.zone)
            add.Run()



# 정보를 받아서 VM 생성 -> 생성되면 이름에 맞춰서 방화벽/포트포워드 추가 -> 포트포워드 완료시 로드밸런서에 추가
class WAS_Add(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'ZoneList', 'display':'VM Zone', 'hr_resid':'name', 'hr_value':_zone['name'], 'reqid':'zoneid', 'resid':'id', 'value':_zone['id']})
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'ProductList', 'display':'VM Spec', 'hr_resid':'serviceofferingdesc', 'hr_value':'', 'reqid':'serviceofferingid', 'resid':'serviceofferingid', 'value':''})
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'TemplateList', 'display':'Image', 'hr_resid':'displaytext', 'hr_value':'', 'reqid':'templateid', 'resid':'id', 'value':''})
        self.param.append({'required':False, 'default':False, 'multiple':True, 'type':'function', 'function':'NetworkList', 'display':'Select CIP', 'hr_resid':'displaytext', 'hr_value':'', 'reqid':'networkids', 'resid':'id', 'value':''})
        self.param.append({'required':False, 'default':False, 'multiple':False, 'type':'function', 'function':'ProductList', 'display':'Disk', 'hr_resid':'diskofferingid', 'hr_value':'', 'reqid':'diskofferingid', 'resid':'diskofferingid', 'value':''})
        self.param.append({'required':True, 'default':False, 'multiple':False, 'type':'manual', 'display':'num of VM', 'data_type':'int', 'hr_value':1, 'reqid':'', 'value':1})
        self.param.append({'required':True, 'default':False, 'multiple':False, 'type':'manual', 'display':'use nas[1-8]', 'data_type':'int', 'hr_value':'', 'reqid':'displayname', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'deployVirtualMachine'
            num_of_server = 1
            name_of_server = ''
            for index, menu in enumerate(self.param):
                if menu['display'] == 'num of VM':
                    num_of_server = menu['value']
                if menu['reqid'] == 'displayname':
                    name_of_server = 'dt-kakao-was-p' + str(menu['value']) + '-node'
                if menu['required'] == False and 'reqid' in menu:
                    if menu['value'] != '':
                        self.data_param[menu['reqid']] = menu['value']
            server_list = CallAPI('server', 'listVirtualMachines', None, 'virtualmachine', [{'field':'displayname', 'search':name_of_server}], None, None, False)
            server_name_map = {}
            for index, vm in enumerate(server_list):
                server_name_map[vm['displayname'][vm['displayname'].index('-node')+5]] = 'O'
            if num_of_server == 1:
                print 'please wait! deploying server #1 ...'
                postfix_of_server = 1
                while str(postfix_of_server) in server_name_map:
                    postfix_of_server += 1
                server_name_map[str(postfix_of_server)] = 'O'
                self.data_param['displayname'] = name_of_server + str(postfix_of_server)
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
            else:
                while num_of_server > 0:
                    print 'please wait! deploying server #' + str(num_of_server) + ' ...'
                    postfix_of_server = 1
                    while str(postfix_of_server) in server_name_map:
                        postfix_of_server += 1
                    server_name_map[str(postfix_of_server)] = 'O'
                    self.data_param['displayname'] = name_of_server + str(postfix_of_server)
                    resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                    MakeAsyncCheck(resp['jobid'], command)
                    num_of_server -= 1
                    if num_of_server > 0:
                        time.sleep(10)
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ProductList' and self.param[_choice-1]['reqid'] == 'diskofferingid':
            serviceofferingid = ''
            for index, menu in enumerate(self.param):
                if menu['reqid'] == 'serviceofferingid':
                    serviceofferingid = menu['value']
            if serviceofferingid != '':
                hr_value = None
                value = None
                hr_value, value = ProductList(self.param[_choice-1], [{'field':'templatedesc', 'search':'Ubuntu 12.04 64bit'}, {'field':'productstate', 'search':'available'}, {'field':'serviceofferingid', 'search':serviceofferingid}])
                if hr_value is not None:
                    self.param[_choice-1]['hr_value'] = hr_value
                if value is not None:
                    self.param[_choice-1]['value'] = value
            else:
                print 'choose VM Spec First!'
                time.sleep(1)
        else:
            BaseDo.SelectParam(self, _choice)



# VM 선택 후 -> 
# VM id로 VM 삭제
# VM name으로 포트포워드 룰에서 사용 중인 ipaddress, publicport를 찾고 포트포워드룰에서 포트포워드룰id로 삭제
# 방화벽룰에서 ipaddress=ipaddress, startport=publicport를 찾고 방화벽룰에서 방화벽룰id로 삭제
# VM name으로 사용중인 로드밸런서를 찾고 로드밸런서id로 서비스웹서버리스트를 찾고 서비스웹서버리스트에서 VM id로 서비스id를 찾아서 제거
class WAS_Remove(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'destroyVirtualMachine'
            server_list = []
            for index_menu, menu in enumerate(self.param):
                if menu['reqid'] == 'id':
                    id_list = menu['value'].split(',')
                    name_list = menu['hr_value'].split(',')
                    list_index = 0
                    for index_virtualmachineid, virtualmachineid in enumerate(id_list):
                        server_list.append({'virtualmachineid':virtualmachineid, 'virtualmachinename':name_list[list_index]})
                        list_index += 1
            for index_vm, vm in enumerate(server_list):
                self.data_param['id'] = vm['virtualmachineid']
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
                #print 'remove VM'
                port_list = CallAPI('server', 'listPortForwardingRules', None, 'portforwardingrule', [{'field':'virtualmachineid', 'search':vm['virtualmachineid']}], None, None, False)
                for index_port, port in enumerate(port_list):
                    #print 'remove portforward ' + port['virtualmachinedisplayname'] + ' -> ' + port['privateport'] + ' : ' + port['publicport']
                    resp_port = CallAPI('server', 'deletePortForwardingRule', {'id':port['id']}, None, None, None, None, False)
                    MakeAsyncCheck(resp_port['jobid'], 'deletePortForwardingRule')
                    firewall_list = CallAPI('server', 'listFirewallRules', None, 'firewallrule', [{'field':'ipaddress', 'search':port['ipaddress']}, {'field':'startport', 'search':port['publicport']}], None, None, False)
                    for index_firewall, firewall in enumerate(firewall_list):
                        #print 'remove firewall ' + firewall['ipaddress'] + ' -> ' + firewall['startport']
                        resp_firewall = CallAPI('server', 'deleteFirewallRule', {'id':firewall['id']}, None, None, None, None, False)
                        MakeAsyncCheck(resp_firewall['jobid'], 'deleteFirewallRule')
                node_nas = vm['virtualmachinename'][14:vm['virtualmachinename'].index('-node')]
                lb_list = CallAPI('lb', 'listLoadBalancers', None, 'loadbalancer', [{'field':'name', 'search':node_nas}], None, None, False)
                for index_lb, lb in enumerate(lb_list):
                    svm_list = CallAPI('lb', 'listLoadBalancerWebServers', {'loadbalancerid':lb['loadbalancerid']}, 'loadbalancerwebserver', [{'field':'virtualmachineid', 'search':vm['virtualmachineid']}], None, None, False)
                    for index_svm, svm in enumerate(svm_list):
                        #print 'remove lb_webserver ' + svm['ipaddress'] + ' -> ' + svm['publicport'] + ' from ' + lb['name']
                        resp_removelb = CallAPI('lb', 'removeLoadBalancerWebServer', {'serviceid':svm['serviceid']}, None, None, None, None, False)
                        if resp_removelb['success'] is True:
                            print 'removeLoadBalancerWebServer complete!'
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ServerList':
            hr_value = None
            value = None
            hr_value, value = ServerList(self.param[_choice-1], [{'field':'state', 'search':'Stopped'}])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        else:
            BaseDo.SelectParam(self, _choice)



class WAS_Start(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'startVirtualMachine'
            server_list = []
            for index, menu in enumerate(self.param):
                if menu['reqid'] == 'id':
                    server_list = menu['value'].split(',')
            for index, menu in enumerate(server_list):
                self.data_param['id'] = menu
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ServerList':
            hr_value = None
            value = None
            hr_value, value = ServerList(self.param[_choice-1], [{'field':'state', 'search':'Stopped'}])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        else:
            BaseDo.SelectParam(self, _choice)



class WAS_Stop(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'stopVirtualMachine'
            server_list = []
            for index, menu in enumerate(self.param):
                if menu['reqid'] == 'id':
                    server_list = menu['value'].split(',')
            for index, menu in enumerate(server_list):
                self.data_param['id'] = menu
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ServerList':
            hr_value = None
            value = None
            hr_value, value = ServerList(self.param[_choice-1], [{'field':'state', 'search':'Running'}])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        else:
            BaseDo.SelectParam(self, _choice)



class WAS_Reboot(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'rebootVirtualMachine'
            server_list = []
            for index, menu in enumerate(self.param):
                if menu['reqid'] == 'id':
                    server_list = menu['value'].split(',')
            for index, menu in enumerate(server_list):
                self.data_param['id'] = menu
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ServerList':
            hr_value = None
            value = None
            hr_value, value = ServerList(self.param[_choice-1], [{'field':'state', 'search':'Running'}])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        else:
            BaseDo.SelectParam(self, _choice)



class WAS_ChangeSpec(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'ProductList', 'display':'VM Spec', 'hr_resid':'serviceofferingdesc', 'hr_value':'', 'reqid':'serviceofferingid', 'resid':'serviceofferingid', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'changeServiceForVirtualMachine'
            server_list = []
            for index, menu in enumerate(self.param):
                if menu['reqid'] == 'id':
                    server_list = menu['value'].split(',')
            for index, menu in enumerate(server_list):
                self.data_param['id'] = menu
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
        return False
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function' and self.param[_choice-1]['function'] == 'ServerList':
            hr_value = None
            value = None
            hr_value, value = ServerList(self.param[_choice-1])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        else:
            BaseDo.SelectParam(self, _choice)