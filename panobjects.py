import requests
import time
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning
import multipleinput
import config
class panorama_objects:
    def __init__(self):
        self.keyv = config.key
        f = multipleinput.multipleinput()
        fields = f.otherfields()
        self.device_group = fields[3] 

    #function to make all changes commit to panorama    
    def commits(self):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        u ="https://<your-panaroma-ip>/api/?type=commit&cmd=<commit></commit>"
        commitresponse = requests.get(u, verify=False, headers={'X-PAN-KEY': self.keyv})
        mycommit = ET.fromstring(commitresponse.content)
        for jobid in mycommit.iter('job'):
            return jobid.text
        time.sleep(3)
        for i in mycommit.iter('msg'):
            return i.text

    #function to make all changes to firewall
    def commits_device(self):
        device_group = self.device_group
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        u ="https://<your-panaroma-ip>/api/?type=commit&action=all&cmd=<commit-all><shared-policy><device-group><entry name="+"'"+device_group+"'"+"/></device-group></shared-policy></commit-all>"
        commitresponse_device = requests.get(u, verify=False, headers={'X-PAN-KEY': self.keyv})
        mycommit_device = ET.fromstring(commitresponse_device.content)
        for jobid in mycommit_device.iter('job'):
            return jobid.text
 #       time.sleep(5)
#        for i in mycommit_device.iter('msg'):
            return i.text

    ###To check if object ip is created
    def address(self,ipa,device_group):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        ipad = "'"+"H-"+ipa+"'"
        u = "https://<your-panaroma-ip>/api/?&type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/address/entry[@name="
        v1 = ipad
        v2 = "]"
        v3 = ""
        url = u+v1+v2+v3
        response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        myroot = ET.fromstring(response.content)
        #Find all
        for counts in myroot.findall('result'):
            data = counts.get('total-count')
            return data

    ###to create object ip
    def create_address(self,ipa,device_group):
        netmsk = ipa+"/32"
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        ipad = "'"+"H-"+ipa+"'"
        u = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/address/entry[@name="
        v1 = ipad
        v2 = "]"
        element = "&element=<ip-netmask>"+netmsk+"</ip-netmask>"
        v3 = ""
        url = u+v1+v2+element+v3
        response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        #return response

###to check ip subnets
    def check_subnet(self,*args):
        ipsub = args[0]
        device_group = args[1]
        addr = ipsub.split("/")
        ipname = addr[0]
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        urlsub = "https://<your-panaroma-ip>/api/?&type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/address/entry[@name=N-"+ipname+"]"
        subresponse = requests.get(urlsub, verify=False, headers={'X-PAN-KEY': self.keyv})
        mysubroot = ET.fromstring(subresponse.content)
	#Find all
        for counts in mysubroot.findall('result'):
            subdata = counts.get('total-count')
            return subdata
            
###to create ip subnets
    def create_subnet(self,*args):
        ipsub = args[0]
        device_group = args[1]
        addr = ipsub.split("/")
        ipname = addr[0]
        mask = addr[1]
        #print(ipname) 
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        urlsub = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/address/entry[@name="+"'"+"N-"+ipname+"_"+mask+"'""]&element=<ip-netmask>"+ipsub+"</ip-netmask>"
        subnetresponse = requests.get(urlsub, verify=False, headers={'X-PAN-KEY': self.keyv})
        mysubroot = ET.fromstring(subnetresponse.content)
        return subnetresponse

###to check  object service
    def service(self,service_name,device_group):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        url = "https://<your-panaroma-ip>/api/?&type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/service/entry[@name="+"'"+service_name+"'""]"
       
        service_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        myroot = ET.fromstring(service_response.content)

#Find all
        for counts in myroot.findall('result'):
            data = counts.get('total-count')
            return data 

###to create object service
    def create_service(self,*args):
        service_name = args[0]
        protocol = args[1]
        dport = args[2]
        device_group = args[3]
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/service/entry[@name="+"'"+service_name+"'""]&element=<protocol><"+protocol+"><port>"+dport+"</port></"+protocol+"></protocol>"

        service_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        #return service_response

###to create schedule   
    def create_schedule(self,*args):
        shcedule_name = args[0]
        #[TimeStamp = time.strftime("%Y%m%d-%H%M"args)]   
        start_date = args[1]
        end_date = args[2]
        device_group = args[3]
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        
        url = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/schedule/entry[@name="+"'"+shcedule_name+"'""]&element=<schedule-type><non-recurring><member>"+start_date+"@00:00-"+end_date+"@23:45</member></non-recurring></schedule-type>"

        schedule_response = requests.get(url, verify=False, headers={'X-PAN-KEY': self.keyv})
        return schedule_response

###to create custom urls
    def create_custom_url(self,*args):
        url_name = str(args[0])
        urlvalue = str(args[1])
        device_group = args[2]
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        urlc = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/profiles/custom-url-category/entry[@name="+"'"+url_name+"'""]&element=<list><member>"+urlvalue+"</member></list><type>URL List</type>"
        print(urlc)
        urlc_response = requests.get(urlc, verify=False, headers={'X-PAN-KEY': self.keyv})
        print("Triggered custom role creation")
        return urlc_response

    def create_custom_wild_url(self,*args):
        url_name = args[0]
        url_name = str(url_name)
        print(type(url_name))
        urlvalue = args[1]
        device_group = args[2]
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        urlc = "https://<your-panaroma-ip>/api/?&type=config&action=set&xpath=/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name="+"'"+device_group+"'"+"]/profiles/custom-url-category/entry[@name="+"'"+url_name+"'""]&element=<list><member>"+urlvalue+"</member></list><type>URL List</type>"
        print(urlc)
        urlc_response = requests.get(urlc, verify=False, headers={'X-PAN-KEY': self.keyv})
        return urlc_response
