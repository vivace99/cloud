# -*- coding: utf-8 -*-
__author__ = 'Edward Lee'

import datetime
import json
import os
import re
import sys
import time
from ucloud import UClient

class Base(object):
    def __init__(self, _api_key, _secret):
        self.api_key = _api_key
        self.secret = _secret
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
    def __init__(self, _api_key, _secret):
        self.api_key = _api_key
        self.secret = _secret
        self.data_param = {}
        self.param = []
        ClearScreen()
        
    def Run(self):
        try:
            while True:
                self.PrintParamMap()
                choice = self.GetMenuChoice(len(self.param)+1)
                if choice == len(self.param)+1:
                    self.Do()
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
                hr_value, value = ServerList(self.api_key, self.secret, self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'ZoneList':
                hr_value, value = ZoneList(self.api_key, self.secret, self.param[_choice-1])
            elif self.param[_choice-1]['function'] == 'ProductList':
                hr_value, value = ProductList(self.api_key, self.secret, self.param[_choice-1], [{'field':'templatedesc', 'search':'Ubuntu 12.04 64bit'}, {'field':'productstate', 'search':'available'}])
            elif self.param[_choice-1]['function'] == 'TemplateList':
                hr_value, value = TemplateList(self.api_key, self.secret, self.param[_choice-1])
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


    
def CallAPI(_api_key, _secret, _api_type, _command, _data_param, _node_name, _filter, _result, _param, _is_print=False):
    client = UClient.UClient(api_type=_api_type, api_key=_api_key, secret=_secret)
    if _data_param is not None:
        resp = client.run(_command, _data_param)
    else:
        resp = client.run(_command)
    if resp is not None:
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

# 서버 리스트 조회
def ServerList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listVirtualMachines'
    data_param = None
    node_name = 'virtualmachine'
    result = ['displayname', 'zonename', 'templatename', 'cpunumber', 'memory', 'state']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 존 리스트 조회
def ZoneList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listZones'
    data_param = None
    node_name = 'zone'
    result = ['name', 'id']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# VM 상품 리스트 조회(Ubuntu 12.04 64bit로 검색)
def ProductList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listAvailableProductTypes'
    data_param = None
    node_name = 'producttypes'
    result = ['product', 'serviceofferingdesc', 'serviceofferingid', 'diskofferingid', 'zonedesc']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 스냅샷 리스트 조회
def SnapshotList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listSnapshots'
    data_param = None
    node_name = 'snapshot'
    result = ['id', 'account', 'name', 'created', 'domain']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 이미지 리스트 조회
def TemplateList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listTemplates'
    data_param = {'templatefilter':'self'}
    node_name = 'template'
    result = ['id', 'account', 'name', 'created', 'domain']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

# 볼륨 리스트 조회
def VolumeList(api_key, secret, param=None, data_filter=None):
    api_type = 'server'
    command = 'listVolumes'
    data_param = None
    node_name = 'volume'
    result = ['id', 'name', 'vmname', 'vmdisplayname', 'vmstate', 'diskofferingid']
    data_list = CallAPI(api_key, secret, api_type, command, data_param, node_name, data_filter, result, param, True)
    if param is not None:
        return SelectParameter(data_list, param)

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