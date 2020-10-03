from netmiko import ConnectHandler
from prettytable import PrettyTable
import socket
import sys
import yaml
from pprint import pprint
from colorama import *
import argparse

import time
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C




class CdpNetMap:
    def __init__(self,Hosts='./Hosts.yaml') :
        self.Hosts = Hosts
        self.KNOWNKEYS = ['host','username','password','device_type']
        self.NONE_NETMIKO_KEYS = ['use_keys','enabled','port','timeout',"key_file"]
        self.DEVICE_INFO = {}
        self.DEVICE_OPTIONS = {}
        try : 
            with open(self.Hosts) as yaml_read:
                self.YAMLdevices = yaml.load(yaml_read, Loader=yaml.FullLoader)
        except FileNotFoundError :
            print(self.Messages('[!] Hosts.yaml File Not Found - Check your filename or path exsistence ','ERROR'))
            sys.exit()
    def StructerData(self):
        self.StructerHOST()
        self.StructerDEFAULT()
        self.DefaultOptions()

    def StructerHOST(self):
        try : 
            Hosts = self.YAMLdevices['hosts']
            ListHosts = list(Hosts.keys())
            for host in ListHosts:
                self.DEVICE_INFO[host] = {}
                self.DEVICE_OPTIONS[host] = {}
                for key in list(Hosts[host].keys()) :
                    if key in self.KNOWNKEYS :
                        self.DEVICE_INFO[host][key] = Hosts[host][key]
                    elif key in self.NONE_NETMIKO_KEYS :
                        self.DEVICE_OPTIONS[host][key] = Hosts[host][key]
                    else :
                        print(self.Messages(f'OPTION_NOTFOUND : Host.yaml Err on host {host} in option "{key}"','ERROR'))
                        sys.exit()
        except KeyError as err :
            print(self.Messages(f'[!] Err in Hosts.yaml , we can\'t read Hosts\n{err}','ERROR'))
    def StructerDEFAULT(self):
        Default = self.YAMLdevices['default']
        for host in list(self.DEVICE_INFO.keys()):
            HOST = self.DEVICE_INFO[host]
            self.DEVICE_OPTIONS[host]
            HOSTKEYS = list(HOST.keys())
            for option in list(Default.keys()) :
                optionNAME = option
                if optionNAME in self.KNOWNKEYS :
                    if optionNAME not in HOSTKEYS :
                        self.DEVICE_INFO[host][optionNAME] = Default[optionNAME]
                elif optionNAME in self.NONE_NETMIKO_KEYS :
                    if optionNAME not in list(self.DEVICE_OPTIONS[host].keys()) :
                        self.DEVICE_OPTIONS[host][optionNAME] = Default[optionNAME]
                else:
                    print(self.Messages(f'OPTION NOTFOUND : Host.yaml Err on Default option => "{optionNAME}"','ERROR'))
                    sys.exit()
    def DefaultOptions(self):
        options = {'use_keys':False,"enable":True,"timeout":5,"port":22,"key_file":'~/.ssh/id_rsa.pub'}
        for device in list(self.DEVICE_OPTIONS.keys()):
            for k , v in options.items():
                if k not in list(self.DEVICE_OPTIONS[device].keys()):
                    self.DEVICE_OPTIONS[device][k] = v
    def ChekDeviceInfo(self,hostname,use_key): # Check evry Host in self.Device_info if he have this : IP/USERNAME/PASSWORD/OS
        KOWNKEYS_CLONE = [i for i in self.KNOWNKEYS]
        NOTFOUND = []
        if use_key == True:
            del KOWNKEYS_CLONE[2]
            for key in KOWNKEYS_CLONE :
                if key in self.DEVICE_INFO[hostname] :
                    pass
                if key not in self.DEVICE_INFO[hostname] :
                    NOTFOUND.append(key)
        elif use_key == False : 
            for key in KOWNKEYS_CLONE :
                if key in self.DEVICE_INFO[hostname] :
                    pass
                if key not in self.DEVICE_INFO[hostname] :
                    NOTFOUND.append(key)
        
        if NOTFOUND :
            return [False,NOTFOUND]
        elif not NOTFOUND :
            return [True,NOTFOUND]
    def CreatConnection(self,hostname,deviceinfo):

        def startconnection(deviceinfo,hostname,enableMode=True):
            print(self.Messages(f'[+] Trying to Establishing SSH Connection with {hostname}','SUCCESSFUL'))
            if enableMode == True :
                conn = ConnectHandler(**deviceinfo)
                conn.enable()
            elif enableMode == False :
                conn = ConnectHandler(**deviceinfo)
            return conn

        use_key = self.DEVICE_OPTIONS[hostname]['use_keys']
        CHECK = self.ChekDeviceInfo(hostname,use_key)
        if CHECK[0] == True :
            FinalDeviceInfo = {}
            FinalDeviceInfo[hostname] = {}
            try : 
                enabled = self.DEVICE_OPTIONS[hostname]['enabled']['secret']
            except Exception:
                enabled = ''
            port = self.DEVICE_OPTIONS[hostname]['port']
            key_file = self.DEVICE_OPTIONS[hostname]['key_file']
            username = deviceinfo['username']
            try :
                password = deviceinfo['password']
            except Exception :
                password = ''
            device_type = deviceinfo['device_type']
            ip = deviceinfo['host']
            if use_key == False :
                if enabled and username and password :
                    FinalDeviceInfo[hostname]['username'] = username
                    FinalDeviceInfo[hostname]['password'] = password
                    FinalDeviceInfo[hostname]['secret'] = enabled
                    FinalDeviceInfo[hostname]['port'] = port
                    FinalDeviceInfo[hostname]['host'] = ip
                    FinalDeviceInfo[hostname]['device_type'] = device_type
                    conn = startconnection(FinalDeviceInfo[hostname],hostname)
                elif not enabled and username and password:
                    FinalDeviceInfo[hostname]['username'] = username
                    FinalDeviceInfo[hostname]['password'] = password
                    FinalDeviceInfo[hostname]['port'] = port
                    FinalDeviceInfo[hostname]['host'] = ip
                    FinalDeviceInfo[hostname]['device_type'] = device_type
                    conn = startconnection(FinalDeviceInfo[hostname],hostname,enableMode=False)
            elif use_key == True :
                if enabled and username and not password :
                    FinalDeviceInfo[hostname]['username'] = username
                    FinalDeviceInfo[hostname]['secret'] = enabled
                    FinalDeviceInfo[hostname]['port'] = port
                    FinalDeviceInfo[hostname]['host'] = ip
                    FinalDeviceInfo[hostname]['use_keys'] = use_key
                    FinalDeviceInfo[hostname]['key_file'] = key_file
                    FinalDeviceInfo[hostname]['device_type'] = device_type
                    conn = startconnection(FinalDeviceInfo[hostname],hostname)
                elif not enabled and username and not password or password:
                    FinalDeviceInfo[hostname]['username'] = username
                    FinalDeviceInfo[hostname]['port'] = port
                    FinalDeviceInfo[hostname]['host'] = ip
                    FinalDeviceInfo[hostname]['use_keys'] = use_key
                    FinalDeviceInfo[hostname]['device_type'] = device_type
                    FinalDeviceInfo[hostname]['key_file'] = key_file
                    conn = startconnection(FinalDeviceInfo[hostname],hostname,enableMode=False)
            return conn
        elif CHECK[0] == False :
            print(self.Messages(f'[!] Please Check your Host.yaml : <<{CHECK[1]}>> option are missing from Host {hostname}','ERROR'))
            return False
    def BasicCDP(self):
        for host in list(self.DEVICE_INFO.keys()) : 
            device = self.DEVICE_INFO[host]
            try:
                connection = self.CreatConnection(host,device)
                if connection != False:
                    print(self.Messages('[+] Start Refreshing CDP information','SUCCESSFUL'))
                    connection.config_mode()
                    connection.send_command('cdp run')
                    connection.send_command('cdp advertise-v2')
                    connection.exit_config_mode()
                    print(self.Messages('[+] Start Collecting Data','SUCCESSFUL'))
                    T = PrettyTable()
                    T.field_names = ["Local", "Local Interface", "Nieghbor", "Nieghbor Interface",'platform','capability']
                    neighbors = connection.send_command("show cdp neighbor", use_genie=True)
                    Count_Directly_Connected = len(list(neighbors['cdp']['index'].keys()))
                    print(f'{host} is directly connected to {Count_Directly_Connected} devices')
                    for Conncted in list(neighbors['cdp']['index'].keys()) :
                        CDPInformation = neighbors['cdp']['index'][Conncted]
                        LocalHost = f'{Conncted}-{host}'
                        T.add_row([LocalHost,CDPInformation['local_interface'],CDPInformation['device_id'],CDPInformation['port_id'],CDPInformation['platform'],CDPInformation['capability']])
                    print(T)
                elif connection == False:
                    pass
            except Exception as err:
                print(self.Messages(f'[!] we could not connect because :\n{err}','ERROR'))
    def DetailCDP(self):
        for host in list(self.DEVICE_INFO.keys()) : 
            device = self.DEVICE_INFO[host]
            try:
                connection = self.CreatConnection(host,device)
                if connection != False:
                    print(self.Messages('[+] Start Refreshing CDP information','SUCCESSFUL'))
                    connection.config_mode()
                    connection.send_command('cdp run')
                    connection.send_command('cdp advertise-v2')
                    connection.exit_config_mode()
                    print(self.Messages('[+] Start Collecting Data','SUCCESSFUL'))
                    neighbors = connection.send_command("show cdp neighbor detail", use_genie=True)
                    Count_Directly_Connected = len(list(neighbors['index'].keys()))
                    print(f'{host} is directly connected to {Count_Directly_Connected} devices')
                    T = PrettyTable()
                    T.field_names = ["L-Hostname", "L-Interface", "N-Hostname", "N-Interface",'N-IP','platform','DeviceType','duplex','Native-Vlan']                
                    for Conncted in list(neighbors['index'].keys()):
                        DEVICE_TYPE = neighbors['index'][Conncted]['capabilities'].split(' ')
                        CDPInformation = neighbors['index'][Conncted]
                        LocalHost = f'{Conncted}-{host}'
                        try : 
                            ManagmentIP = list(CDPInformation['entry_addresses'].keys())[0]
                        except Exception as err :
                            ManagmentIP = None
                        if 'Router' in DEVICE_TYPE and 'Switch' not in DEVICE_TYPE :
                            T.add_row([LocalHost,CDPInformation['local_interface'],CDPInformation['device_id'],CDPInformation['port_id'],ManagmentIP,CDPInformation['platform'],"Router",CDPInformation['duplex_mode'],CDPInformation['native_vlan']])
                        elif 'Router' in DEVICE_TYPE and 'Switch' in DEVICE_TYPE:
                            T.add_row([LocalHost,CDPInformation['local_interface'],CDPInformation['device_id'],CDPInformation['port_id'],ManagmentIP,CDPInformation['platform'],'L3 Switch',CDPInformation['duplex_mode'],CDPInformation['native_vlan']])
                        elif 'Router' not in DEVICE_TYPE and "Switch" in DEVICE_TYPE:
                            T.add_row([LocalHost,CDPInformation['local_interface'],CDPInformation['device_id'],CDPInformation['port_id'],ManagmentIP,CDPInformation['platform'],'L2 Switch',CDPInformation['duplex_mode'],CDPInformation['native_vlan']])
                        else : 
                            T.add_row([LocalHost,CDPInformation['local_interface'],CDPInformation['device_id'],CDPInformation['port_id'],ManagmentIP,CDPInformation['platform'],CDPInformation['capabilities'],CDPInformation['native_vlan']])

                    print(T)
                elif connection == False :
                    pass
            except Exception as err:
                print(self.Messages(f'[!] we could not connect because :\n{err}','ERROR'))

    def Messages(self,msg,type_message):
        if type_message == 'ERROR':
            return Fore.LIGHTRED_EX+msg+Style.RESET_ALL
        elif type_message == 'SUCCESSFUL':
            return Fore.GREEN+msg+Style.RESET_ALL

start = CdpNetMap()

if len(sys.argv) > 1 :

    parser = argparse.ArgumentParser(description='CDP network Discovery')
    parser.add_argument('-B',"--Basic",help='For Basic CDP information',action='store_true')
    parser.add_argument('-D',"--Detail",help='For Detailed CDP information',action='store_true')
    args = parser.parse_args()
    if len(sys.argv) <= 2 :
        for k in args._get_kwargs() :
            if k[0] == 'Basic' and k[1]==True:
                start.StructerData()
                start.BasicCDP()
            elif k[0]== 'Detail' and k[1]==True:
                start.StructerData()
                start.DetailCDP()
    elif len(sys.argv) > 2 :
        print(start.Messages('[!] Please Use one Argument','ERROR'))
else: 
    print(start.Messages('[!] Use -h for help','ERROR'))