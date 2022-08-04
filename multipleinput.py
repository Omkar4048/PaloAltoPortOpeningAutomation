##################
#script in python
#script to get multiple inputs and keep it into variables to call later
##################

from datetime import datetime
import sys
#import urlcheck

class multipleinput:

    def __init__(self):					#it will first defile all required variables from input arguments
        self.Source_Ip = sys.argv[1]
        self.Dest_Ip = sys.argv[2]
        self.service_name = sys.argv[3]
        self.service_port = sys.argv[4]
        self.rulename = sys.argv[5]
        self.description = sys.argv[6]
        #self.t1_value = sys.argv[7]
        #self.t2_value = sys.argv[8]
        self.numberdays = sys.argv[7]
        #self.protocol = sys.argv[8]
        self.device_group = sys.argv[8]

    def multip(self):						#function created to create list of SIP and DIP
        siplist = []
        diplist = []
        Source_Ip_List = self.Source_Ip.split(",")
        Dest_Ip_List = self.Dest_Ip.split(",")
        for i in Source_Ip_List:
            siplist.append(i)
        for j in Dest_Ip_List:
            diplist.append(j)
 #           url_check=urlcheck.check_url(j)
  #          if url_check:
   #           print("URL entered: ",j)
        siplength = len(siplist)
        diplength = len(diplist)
        return siplength, diplength, siplist, diplist

    def multiport(self):					#function created to create list of ports
        #service_name_list = []
        service_port_list = []
        servicename = self.service_name.lower()
        serviceport = self.service_port.split(",")
        #for i in servicename:
         #   service_name_list.append(i)
        for j in serviceport:
            service_port_list.append(j)
        #servicenamelength = len(service_name_list)
        serviceportlength = len(service_port_list)
        return  serviceportlength, servicename, service_port_list
	
    def otherfields(self):					#this will define all other required arguments
        rule_name = self.rulename
        descriptiondata = self.description
        #t1_value = self.t1_value
        #t2_value = self.t2_value
        numberdays = self.numberdays
        devicegroup = self.device_group
        #print("devicegroup in other fields multiinputfile "+devicegroup )
        return rule_name, descriptiondata, numberdays, devicegroup
