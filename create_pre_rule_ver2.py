import requests
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning
import sys
import config

###To disable Insecure ssl warnings
class panorama_prerule:
    def __init__(self):
        self.keyv = config.key

    def checkrulepresent(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        rulename = args[0]
        device_group = args[1]
        url = "https://<your-panaroma-ip>/api/?&type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]"
        response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        myroot = ET.fromstring(response.content)
        
        for counts in myroot.findall('result'):
            data = counts.get('total-count')
            return data

    def checkdevicerulepresent(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        rulename = args[0]
        device_group = args[1]
        url = "https://<your-paloaltodevice-ip>/api/?&type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]"
        response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        myroot = ET.fromstring(response.content)

        for counts in myroot.findall('result'):
            data = counts.get('total-count')
            return data
            
################################################################
####To Create port open rule for single sip dip 
    def create_port_open_prerule(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        rulename = args[0]
        sip = args[1]
        dip = args[2]
        servicename = args[3]
        descriptions = args[4]
        t1 = args[5]
        t2 = args[6]
        t3 = args[7]
        t4 = args[8]
        device_group = args[9]
        #print(device_group)
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]&element=<source><member>"+sip+"</member></source><destination><member>"+dip+"</member></destination><service><member>"+servicename+"</member></service><application><member>any</member></application><action>allow</action><source-user><member>any</member></source-user><description>"+descriptions+"</description><from><member>"+t1+"</member></from><from><member>"+t2+"</member></from><to><member>"+t3+"</member></to><to><member>"+t4+"</member></to><profile-setting><group><member>ICICI-Azure</member></group></profile-setting><log-setting>ICICI-SIEM</log-setting>"
        response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
#        file_path = 'rulecreate.log'
#        sys.stdout =  open(file_path, "a")
        print(response.content)

###Create Temp rule with schedule
    
    def create_port_open_prerule_tmp(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        print("temp rule creation call executed!!!")
        rulename = args[0]
        sip = args[1]
        dip = args[2]
        servicename = args[3]
        descriptions = args[4]
        t1 = args[5]
        t2 = args[6]
        t3 = args[7]
        t4 = args[8]
        scheduler = args[9]
        device_group = args[10]
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]&element=<source><member>"+sip+"</member></source><destination><member>"+dip+"</member></destination><service><member>"+servicename+"</member></service><application><member>any</member></application><action>allow</action><source-user><member>any</member></source-user><description>"+descriptions+"</description><from><member>"+t1+"</member></from><from><member>"+t2+"</member></from><to><member>"+t3+"</member></to><to><member>"+t4+"</member></to><profile-setting><group><member>ICICI-Azure</member></group></profile-setting><log-setting>ICICI-SIEM</log-setting><schedule>"+scheduler+"</schedule>"
        tmp_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
 #       file_path = 'rulecreate.log'
  #      sys.stdout =  open(file_path, "a")
        print(tmp_response.content)
    
###Create URL Whitelisting policy

    def create_url_whitelist(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        rulename = args[0]
        sip = args[1]
        descriptions = args[2]
        t1 = args[3]
        t2 = args[4]
        categoryurl = args[5]
        device_group = args[6]
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]&element=<source><member>"+sip+"</member></source><destination><member>any</member></destination><service><member>application-default</member></service><application><member>any</member></application><action>allow</action><source-user><member>any</member></source-user><description>"+descriptions+"</description><from><member>"+t1+"</member></from><to><member>"+t2+"</member></to><profile-setting><group><member>ICICI-Azure</member></group></profile-setting><log-setting>ICICI-SIEM</log-setting><category><member>"+categoryurl+"</member></category>"

        url_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
     #   file_path = 'rulecreate.log'
     #   sys.stdout =  open(file_path, "a")
        print(url_response.content)

###Create url whitelist with scheduler
    
    def create_url_whitelist_tmp(self,*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        rulename = args[0]
        sip = args[1]
        descriptions = args[2]
        t1 = args[3]
        t2 = args[4]
        categoryurl = args[5]
        scheduler = args[6]
        device_group = args[7]
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/pre-rulebase/security/rules/entry[@name="+"'"+rulename+"'""]&element=<source><member>"+sip+"</member></source><destination><member>any</member></destination><service><member>application-default</member></service><application><member>any</member></application><action>allow</action><source-user><member>any</member></source-user><description>"+descriptions+"</description><from><member>"+t1+"</member></from><to><member>"+t2+"</member></to><profile-setting><group><member>ICICI-Azure</member></group></profile-setting><log-setting>ICICI-SIEM</log-setting><category><member>"+categoryurl+"</member></category><schedule>"+scheduler+"</schedule>"

        url_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
     #   file_path = 'rulecreate.log'
     #   sys.stdout =  open(file_path, "a")
        print(url_response.content)
