# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

import datetime
import json
import os
import re
import sys
import time
import thread
from ucloud import UClient

SERVICE_IP = '14.63.170.144'
UCLOUD_API_KEY = 'XJgePBKStnGIVB5MwNnsRx9a-WsUNAWgOLsudCMOsgCvkKqyAsViM4Jxr-aZgvt6UfpB74Jgbj2XES0zbQ3kng'
UCLOUD_SECRET  = 'uGBRE4pFXUGhnjaz-x1HDKefJAP1m6KKVXTM-mJXWr0K78VtySzFN4Nn9XNPjKqqB7GVI_gEY1lYoN3qEWY-CA'
WELL_KNOWN_HTTP = 80
WELL_KNOWN_HTTPS = 443

class Base(object):
    def __init__(self):
        self.menus = []
        ClearScreen()
        
    def Run(self):
        try:
            while True:
                self.PrintMenu()
                choice = self.GetMenuChoice(len(self.menus))
                if choice == len(self.menus):
                    ClearScreen()
                    return
                else:
                    self.RunMenu(choice)
        except KeyboardInterrupt:
            ClearScreen()
            return
    
    def RunMenu(self, _choice):
        print 'run class specific method'
    
    def GetMenuChoice(self, max):
        while True:
            input = raw_input('> ')
            try:
                num = int(input)
            except ValueError:
                print 'Invalid choice. Please choose a value between 1 and', max
                continue
            if num > max or num < 1:
                print 'Invalid choice. Please choose a value between 1 and', max
            else:
                return num
    
    def PrintMenu(self):
        title = self.__class__.__name__ + ' Management'
        PrintLine(len(title))
        print title
        PrintLine(len(title))
        for index, menu in enumerate(self.menus):
            print str(index+1) + ') ' + menu



class BaseDo(object):
    def __init__(self):
        self.data_param = {}
        self.param = []
        ClearScreen()
        
    def Run(self):
        try:
            while True:
                self.PrintParamMap()
                choice = self.GetMenuChoice(len(self.param)+1)
                if choice == len(self.param)+1:
                    if self.Do() is True:
                        return
                else:
                    self.SelectParam(choice)
        except KeyboardInterrupt:
            ClearScreen()
            return
    
    def Do(self):
        is_fill = True
        required = ''
        for index, menu in enumerate(self.param):
            if menu['default'] is True:
                self.data_param[menu['reqid']] = menu['value']
            if menu['required'] is True and menu['value'] == '':
                is_fill = False
                required = menu['display']
                break
        if is_fill is False:
            print required + ' is empty!'
            time.sleep(1)
        return is_fill
    
    def SelectParam(self, _choice):
        if self.param[_choice-1]['type'] == 'function':
            hr_value = None
            value = None
            if self.param[_choice-1]['function'] == 'ServerList':
                hr_value, value = ServerList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'ZoneList':
                hr_value, value = ZoneList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'ProductList':
                hr_value, value = ProductList(self.param[_choice-1], [{'field':'templatedesc', 'search':'Ubuntu 12.04 64bit'}, {'field':'productstate', 'search':'available'}])
            elif self.param[_choice-1]['function'] == 'TemplateList':
                hr_value, value = TemplateList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'NetworkList':
                hr_value, value = NetworkList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'AddressList':
                hr_value, value = AddressList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'FireWallList':
                hr_value, value = FireWallList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'PortForwardList':
                hr_value, value = PortForwardList(self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'LoadBalancerList':
                hr_value, value = LoadBalancerList(self.param[_choice-1])
            if hr_value is not None:
                self.param[_choice-1]['hr_value'] = hr_value
            if value is not None:
                self.param[_choice-1]['value'] = value
        elif self.param[_choice-1]['type'] == 'manual':
            ClearScreen()
            title = 'insert ' + self.param[_choice-1]['display']
            PrintLine(len(title))
            print title
            PrintLine(len(title))
            value = GetInput(self.param[_choice-1]['data_type'])
            if value is not None:
                self.param[_choice-1]['hr_value'] = value
                self.param[_choice-1]['value'] = value
        elif self.param[_choice-1]['type'] == 'static':
            print 'can not change static value!'
            time.sleep(1)
    
    def GetMenuChoice(self, max):
        while True:
            input = raw_input('> ')
            try:
                num = int(input)
            except ValueError:
                print 'Invalid choice. Please choose a value between 1 and', max
                continue
            if num > max or num < 1:
                print 'Invalid choice. Please choose a value between 1 and', max
            else:
                return num
    
    def PrintParamMap(self):
        ClearScreen()
        separator = ' : '
        field_size = {'index':0, 'name':0, 'value':0}
        line_length = 0
        title = self.__class__.__name__
        line_length = len(title)
        last_index = 0
        for index, menu in enumerate(self.param):
            last_index = index
            if len(str(index)) > field_size['index']:
                field_size['index'] = len(str(index))
            if len(menu['display']) > field_size['name']:
                field_size['name'] = len(menu['display'])
            if len(str(menu['hr_value'])) > field_size['value']:
                field_size['value'] = len(str(menu['hr_value']))
        last_index += 1
        if len(str(last_index)) > field_size['index']:
            field_size['index'] = len(str(last_index))
        line_length = field_size['index'] + 2 + field_size['name'] + len(separator) + field_size['value']
        PrintLine(line_length)
        PrintChar(int((line_length-len(title))/2))
        print title
        PrintLine(line_length)
        last_index = 0
        for index, menu in enumerate(self.param):
            last_index = index
            PrintChar(field_size['index']-len(str(index+1)))
            sys.stdout.write(str(index+1) + ') ')
            PrintChar(field_size['name']-len(menu['display']))
            print menu['display'] + separator + str(menu['hr_value'])
        last_index += 1
        print str(last_index+1) + ') Run!'



########## 비동기 쓰레드 함수 ##########
def MakeAsyncCheck(_jobid, _command):
    try:
        thread.start_new_thread( CheckAsync, (_jobid, _command, ) )
    except:
        print "Error: unable to start thread"

def CheckAsync(_jobid, _command):
    while True:
        time.sleep(10)
        result = CallAPI('server', 'queryAsyncJobResult', {'jobid':_jobid}, None, None, None, None, False)
        if result is not None:
            if 'jobstatus' in result:
                if result['jobstatus'] == 0:
                    continue
                elif result['jobstatus'] == 1:
                    print _command + ' complete!'
                    print result
                    if 'jobresult' in result:
                        if _command == 'deployVirtualMachine':
                            if 'virtualmachine' in result['jobresult']:
                                CBdeployVirtualMachine(result['jobresult']['virtualmachine'])
                        elif _command == 'createPortForwardingRule':
                            if 'portforwardingrule' in result['jobresult']:
                                CBcreatePortForwardingRule(result['jobresult']['portforwardingrule'])
                    return
                elif result['jobstatus'] == 2:
                    print 'fail'
                    return
                else:
                    print 'error'
                    return
        else:
            print 'error'
            return

########## API 호출 함수 ##########
def CallAPI(_api_type, _command, _data_param, _node_name, _filter, _result, _param, _is_print=False):
    client = UClient.UClient(api_type=_api_type, api_key=UCLOUD_API_KEY, secret=UCLOUD_SECRET)
    if _data_param is not None:
        for _item in _data_param:
            if isinstance(_data_param[_item], int) is True:
                _data_param[_item] = str(_data_param[_item])
        resp = client.run(_command, _data_param)
    else:
        resp = client.run(_command)
    #print resp
    if resp is not None:
        if 'errorcode' in resp:
            PrintAPIError(resp)
            return None
        real_resp = None
        if _node_name is not None:
            if _node_name in resp:
                real_resp = resp[_node_name]
            else:
                return None
        else:
            real_resp = resp
        filtered_data = []
        if _filter is not None:
            data_list = DataFilter(real_resp, _filter)
            if _is_print is True:
                PrintList(data_list, _result)
        else:
            data_list = real_resp
            if _is_print is True:
                PrintList(data_list, _result)
        return data_list
    else:
        PrintLog(_node_name + ' does not exist!')
        return None

def PrintAPIError(_error):
    print _error['errortext']
    time.sleep(1)
    ClearScreen()

########## 사용자 입력 함수 ##########
# 데이터 중 하나를 선택해서 원하는 parameter를 반환
def SelectParameter(data_list, param):
    if len(data_list) == 0:
        return (None, None)
    else:
        try:
            while True:
                allow_multi = False
                if param is not None and 'multiple' in param:
                    allow_multi = param['multiple']
                choice = GetSelectedNumber(len(data_list), allow_multi)
                choice_list = choice.split(',')
                hr_resid = ''
                resid = ''
                for index, choice_index in enumerate(choice_list):
                    selected_data = data_list[int(choice_index)-1]
                    if hr_resid != '':
                        hr_resid += ','
                    if param['hr_resid'] in selected_data:
                        hr_resid += selected_data[param['hr_resid']]
                    if resid != '':
                        resid += ','
                    if param['resid'] in selected_data:
                        resid += selected_data[param['resid']]
                return (hr_resid, resid)
        except KeyboardInterrupt:
            return (None, None)

# 리스트 선택 번호 입력
def GetSelectedNumber(max, allow_multi=False):
    while True:
        input = raw_input('> ')
        if allow_multi is True:
            input_list = input.split(',')
            is_valid = True
            for index, value in enumerate(input_list):
                try:
                    num = int(value)
                    if num > max or num < 1:
                        is_valid = False
                except ValueError:
                    is_valid = False
            if is_valid is True:
                return input
            else:
                print 'Invalid choice. Please choose a value between 1 and', max
        else:
            try:
                num = int(input)
            except ValueError:
                print 'Invalid choice. Please choose a value between 1 and', max
                continue
            if num > max or num < 1:
                print 'Invalid choice. Please choose a value between 1 and', max
            else:
                return input

# 사용자 입력
def GetInput(type):
    try:
        while True:
            if type == 'int':
                choice = GetInputInt()
            elif type == 'string':
                choice = GetInputString()
            return choice
    except KeyboardInterrupt:
        return None

# 정수 입력
def GetInputInt():
    while True:
        input = raw_input('> ')
        try:
            num = int(input)
        except ValueError:
            print 'only integer allowed'
            continue
        return num

# 문자열 입력
def GetInputString():
    while True:
        input = raw_input('> ')
        try:
            if len(input) == 0:
                print 'more than 1 character need'
                continue
            if bool(re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣_ ]+.*', input)) is True:
                print 'only english and - allowed'
                continue
        except ValueError:
            print 'only string allowed'
            continue
        return input

########## API 호출 함수 ##########
# 서버 리스트 조회
def ServerList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listVirtualMachines'
    data_param = None
    node_name = 'virtualmachine'
    result = ['displayname', 'zonename', 'templatename', 'cpunumber', 'memory', 'state']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 존 리스트 조회
def ZoneList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listZones'
    data_param = None
    node_name = 'zone'
    result = ['name', 'id']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# VM 상품 리스트 조회(Ubuntu 12.04 64bit로 검색)
def ProductList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listAvailableProductTypes'
    data_param = None
    node_name = 'producttypes'
    result = ['product', 'serviceofferingdesc', 'serviceofferingid', 'diskofferingid', 'zonedesc']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 스냅샷 리스트 조회
def SnapshotList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listSnapshots'
    data_param = None
    node_name = 'snapshot'
    result = ['id', 'account', 'name', 'created', 'domain']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 이미지 리스트 조회
def TemplateList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listTemplates'
    data_param = {'templatefilter':'self'}
    node_name = 'template'
    result = ['id', 'account', 'name', 'created', 'domain']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 볼륨 리스트 조회
def VolumeList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listVolumes'
    data_param = None
    node_name = 'volume'
    result = ['id', 'name', 'vmname', 'vmdisplayname', 'vmstate', 'diskofferingid']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 네트워크 리스트 조회
def NetworkList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listNetworks'
    data_param = None
    node_name = 'network'
    result = ['id', 'name', 'displaytext', 'canusefordeploy', 'cidr', 'gateway', 'netmask']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 아이피 리스트 조회
def AddressList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listPublicIpAddresses'
    data_param = None
    node_name = 'publicipaddress'
    result = ['id', 'ipaddress', 'zonename', 'domain']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    print data_list
    if param is not None:
        return SelectParameter(data_list, param)

# 방화벽 리스트 조회
def FireWallList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listFirewallRules'
    data_param = None
    node_name = 'firewallrule'
    result = ['ipaddress', 'startport', 'endport', 'protocol', 'cidrlist', 'state']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 포트 포워드 리스트 조회
def PortForwardList(param=None, data_filter=None):
    api_type = 'server'
    command = 'listPortForwardingRules'
    data_param = None
    node_name = 'portforwardingrule'
    result = ['ipaddress', 'publicport', 'virtualmachinedisplayname', 'privateport', 'state']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 로드밸런서 리스트 조회
def LoadBalancerList(param=None, data_filter=None):
    api_type = 'lb'
    command = 'listLoadBalancers'
    data_param = None
    node_name = 'loadbalancer'
    result = ['name', 'serviceip', 'serviceport', 'loadbalanceroption', 'state']
    data_list = CallAPI(api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

########## 콜백 함수 ##########
def CBdeployVirtualMachine(result):
    if '-was-' in result['displayname']:
        # new WAS VM
        node_id = result['id']
        node_name = result['displayname']
        node_nas = int(node_name[14:node_name.index('-node')])
        node_number = int(node_name[node_name.index('-node')+5])
        # get used port for service
        port_used = CallAPI('server', 'listPortForwardingRules', None, 'portforwardingrule', [{'field':'ipaddress', 'search':SERVICE_IP}], None, None, False)
        ipaddressid = ''
        port_http = WELL_KNOWN_HTTP
        port_https = WELL_KNOWN_HTTPS
        port_http_map = {}
        port_https_map = {}
        for index, row in enumerate(port_used):
            ipaddressid = row['ipaddressid']
            if int(row['publicport']) < WELL_KNOWN_HTTPS:
                port_http_map[row['publicport']] = 'O'
            else:
                port_https_map[row['publicport']] = 'O'
        while str(port_http) in port_http_map:
            port_http += 1
        while str(port_https) in port_https_map:
            port_https += 1
        # regist http & https firewall rule
        CallAPI('server', 'createFirewallRule', {'ipaddressid':ipaddressid, 'protocol':'TCP', 'startport':port_http, 'endport':port_http}, None, None, None, None, False)
        CallAPI('server', 'createFirewallRule', {'ipaddressid':ipaddressid, 'protocol':'TCP', 'startport':port_https, 'endport':port_https}, None, None, None, None, False)
        # regist http & https port forward rule
        resp = CallAPI('server', 'createPortForwardingRule', {'ipaddressid':ipaddressid, 'privateport':WELL_KNOWN_HTTP, 'protocol':'TCP', 'publicport':port_http, 'virtualmachineid':result['id']}, None, None, None, None, False)
        MakeAsyncCheck(resp['jobid'], 'createPortForwardingRule')
        resp = CallAPI('server', 'createPortForwardingRule', {'ipaddressid':ipaddressid, 'privateport':WELL_KNOWN_HTTPS, 'protocol':'TCP', 'publicport':port_https, 'virtualmachineid':result['id']}, None, None, None, None, False)
        MakeAsyncCheck(resp['jobid'], 'createPortForwardingRule')
    elif '-cass-' in result['displayname']:
        # new cassandra Node
        print 'new cassandra Node'

def CBcreatePortForwardingRule(result):
    # new WAS VM
    node_id = result['virtualmachineid']
    node_name = result['virtualmachinedisplayname']
    node_nas = node_name[14:node_name.index('-node')]
    node_ip = result['ipaddress']
    node_port = result['publicport']
    node_search = ''
    if int(node_port) < WELL_KNOWN_HTTPS:
        node_search = 'http' + node_nas
    else:
        node_search = 'https' + node_nas
    # get used load balancer
    lb_used = CallAPI('lb', 'listLoadBalancers', None, 'loadbalancer', [{'field':'name', 'search':node_search}], None, None, False)
    loadbalancerid = ''
    for index, row in enumerate(lb_used):
        loadbalancerid = row['loadbalancerid']
    # regist http & https firewall rule
    CallAPI('lb', 'addLoadBalancerWebServer', {'loadbalancerid':loadbalancerid, 'virtualmachineid':node_id, 'ipaddress':node_ip, 'publicport':node_port}, None, None, None, None, False)

########## 유틸 함수 ##########
def DataFilter(_list, _filter):
    new_list = []
    for i, data in enumerate(_list):
        is_pass = True
        for j, search in enumerate(_filter):
            if search['search'] not in data[search['field']]:
                is_pass = False
                break
        if is_pass is True:
            new_list.append(data)
    return new_list

def PrintLog(_message):
    ClearScreen()
    print _message

def PrintLine(_size):
    i = 0
    line = ''
    for i in range(_size):
        line += '-'
    print line
    
def PrintChar(_size, _char=' '):
    for i in range(_size):
        sys.stdout.write(_char)

def PrintList(_list, _fields):
    ClearScreen()
    separator = ' | '
    field_size = {'index':1}
    line_length = 0
    for field in _fields:
        field_size[field] = len(field)
    for index, menu in enumerate(_list):
        if len(str(index+1)) > field_size['index']:
            field_size['index'] = len(str(index+1))
        for field in _fields:
            if field in menu and len(str(menu[field])) > field_size[field]:
                field_size[field] = len(str(menu[field]))
    line_length += field_size['index'] + len(separator)
    for field in _fields:
        line_length += field_size[field] + len(separator)
    PrintLine(line_length+1)
    PrintChar(int((line_length+1-len(sys._getframe(2).f_code.co_name)-4)/2))
    print '* ' + sys._getframe(2).f_code.co_name + ' *'
    PrintLine(line_length+1)
    sys.stdout.write('| ')
    PrintChar(field_size['index'])
    sys.stdout.write(separator)
    for field in _fields:
        if len(field) < field_size[field]:
            PrintChar(field_size[field]-len(field))
        sys.stdout.write(field + separator)
    print ''
    PrintLine(line_length+1)
    for index, menu in enumerate(_list):
        line = ''
        sys.stdout.write('| ')
        if len(str(index+1)) < field_size['index']:
            PrintChar(field_size['index']-len(str(index+1)))
        sys.stdout.write(str(index+1) + separator)
        for field in _fields:
            if field in menu:
                if len(str(menu[field])) < field_size[field]:
                    PrintChar(field_size[field]-len(str(menu[field])))
                sys.stdout.write(str(menu[field]) + separator)
            else:
                PrintChar(field_size[field])
                sys.stdout.write(separator)
        print ''
    PrintLine(line_length+1)
    print ''

def ClearScreen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')