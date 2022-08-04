import requests
import time
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning
import sys
import os
import config

class paloalto_objects:
    def commits_paloalto():
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        u ="https://<your-device-ip>/api/?type=commit&cmd=<commit></commit>"
        commitresponse = requests.get(u, verify=False, headers={'X-PAN-KEY': config.key})
        mycommit = ET.fromstring(commitresponse.content)
        for jobid in mycommit.iter('job'):
            return jobid.text
        time.sleep(3)
        for i in mycommit.iter('msg'):
            return i.text

###To check if object ip is created
    def create_route_ip(*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        rname = args[0]
        ipas = args[1]
        ipad = ipas+"/32"
        rulename = rname+"_"+ipas
        u = "https://<your-device-ip>/api/?type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/routing-table/ip/static-route/entry[@name="+"'"+rulename+"'""]&element=<nexthop><ip-address>10.227.0.81</ip-address></nexthop><bfd><profile>None</profile></bfd><path-monitor><enable>no</enable><failure-condition>any</failure-condition><hold-time>2</hold-time></path-monitor><interface>ethernet1/1</interface><metric>10</metric><destination>"+ipad+"</destination><route-table><unicast"+'/'+"></route-table>"
        response = requests.get(u, verify=False, headers={'X-PAN-KEY': config.key})
        print(response.content)

    def create_route_subnetip(*args):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        rname = args[0]
        ipas = args[1]
        sub = ipas.split("/")
        ipsingle = sub[0]
        ipsub = sub[1]
        rulename = rname+"_"+ipsingle+"_"+ipsub
        u = "https://<your-device-ip>/api/?type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/routing-table/ip/static-route/entry[@name="+"'"+rulename+"'""]&element=<nexthop><ip-address>10.227.0.81</ip-address></nexthop><bfd><profile>None</profile></bfd><path-monitor><enable>no</enable><failure-condition>any</failure-condition><hold-time>2</hold-time></path-monitor><interface>ethernet1/1</interface><metric>10</metric><destination>"+ipas+"</destination><route-table><unicast"+'/'+"></route-table>"
        response = requests.get(u, verify=False, headers={'X-PAN-KEY': config.key})
        print(response.content)
