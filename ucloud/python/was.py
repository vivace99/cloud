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



class WAS_Add(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'ZoneList', 'display':'VM Zone', 'hr_resid':'name', 'hr_value':_zone['name'], 'reqid':'zoneid', 'resid':'id', 'value':_zone['id']})
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'ProductList', 'display':'VM Spec', 'hr_resid':'serviceofferingdesc', 'hr_value':'', 'reqid':'serviceofferingid', 'resid':'serviceofferingid', 'value':''})
        self.param.append({'required':True, 'default':True, 'multiple':False, 'type':'function', 'function':'TemplateList', 'display':'Image', 'hr_resid':'displaytext', 'hr_value':'', 'reqid':'templateid', 'resid':'id', 'value':''})
        self.param.append({'required':False, 'default':False, 'multiple':True, 'type':'function', 'function':'NetworkList', 'display':'Select CIP', 'hr_resid':'displaytext', 'hr_value':'', 'reqid':'networkids', 'resid':'id', 'value':''})
        self.param.append({'required':False, 'default':False, 'multiple':False, 'type':'function', 'function':'ProductList', 'display':'Disk', 'hr_resid':'diskofferingid', 'hr_value':'', 'reqid':'diskofferingid', 'resid':'diskofferingid', 'value':''})
        self.param.append({'required':True, 'default':False, 'multiple':False, 'type':'manual', 'display':'num of VM', 'data_type':'int', 'hr_value':1, 'reqid':'', 'value':1})
        self.param.append({'required':True, 'default':False, 'multiple':False, 'type':'manual', 'display':'VM name prefix', 'data_type':'string', 'hr_value':'', 'reqid':'displayname', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'deployVirtualMachine'
            num_of_server = 1
            name_of_server = 'DT-WAS-GP1'
            for index, menu in enumerate(self.param):
                if menu['display'] == 'num of VM':
                    num_of_server = menu['value']
                if menu['reqid'] == 'displayname':
                    name_of_server = menu['value']
                if menu['required'] == False and 'reqid' in menu:
                    if menu['value'] != '':
                        self.data_param[menu['reqid']] = menu['value']
            if num_of_server == 1:
                self.data_param['displayname'] = name_of_server
                resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                MakeAsyncCheck(resp['jobid'], command)
            else:
                while num_of_server > 0:
                    self.data_param['displayname'] = name_of_server + '-' + str(num_of_server)
                    resp = CallAPI(api_type, command, self.data_param, None, None, None, None, False)
                    MakeAsyncCheck(resp['jobid'], command)
                    num_of_server -= 1
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



class WAS_Remove(BaseDo):
    def __init__(self, _zone):
        BaseDo.__init__(self)
        self.param.append({'required':True, 'default':True, 'multiple':True, 'type':'function', 'function':'ServerList', 'display':'Select VM', 'hr_resid':'displayname', 'hr_value':'', 'reqid':'id', 'resid':'id', 'value':''})
    
    def Do(self):
        if BaseDo.Do(self) is True:
            api_type = 'server'
            command = 'destroyVirtualMachine'
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