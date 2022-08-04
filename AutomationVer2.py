##############################################################
##Scripted By Omkar Kamble
##############################################################

###*****************Import Important Module******************##
import multipleinput
import checkipadd
import panobjects
import ipaddress
import create_pre_rule_ver2
from routecheck import routecheck
import contextlib
import datetime
import time
import sys

######***************Taking Input*******************######
f = multipleinput.multipleinput()                   #Input segregation module
fields = f.otherfields()                            #Taking fields from module to assign

rulename = fields[0]                                #All variable assignment to use it later
description = fields[1]
number_days = fields[2]
#serviceprotocol = fields[3]
device_group = fields[3]

ips = f.multip()                                    #getting all ip details from all input
sipcount = ips[0]
dipcount = ips[1]
siplist = ips[2]
diplist = ips[3]
iplist= siplist+diplist

services = f.multiport()                            #extract single/multiple port details
#servicenamecount = services[0]
serviceportcount = services[0]
serviceprotocol = services[1]
serviceportlist = services[2]

####*************Prerequisite*****************###
siptype = []
diptype = []
zsiplist = []
zdiplist = []
ip_exist=""
ip_existlist = []
service_name_list = []
sip_name_list = []
dip_name_list = []
#siplist=[x for x in siplist if x]
#diplist=[x for x in diplist if x]
#print(siplist)
#print(diplist)
p = panobjects.panorama_objects()                        #Object Creation Module
prerule = create_pre_rule_ver2.panorama_prerule()        #Rule Creation Module

#####***Log for Input Parameters********################
now = datetime.datetime.now()
date_time = now.strftime("%d/%m/%Y %H:%M:%S")
all_parameter = open('<Pathofyourscript>/scripttriggerlogs.txt', 'a')       #this step is executed to redirect all input parameters to file
all_parameter.write("\n")
all_parameter.write("Script Trigerred On:")
all_parameter.write(str(date_time))
all_parameter.write(str(fields))
all_parameter.write(str(ips))
all_parameter.write(str(services))
all_parameter.write("\n")
all_parameter.close()

###*****Checking given Argument type is URL, IPaddress or Network*************##
for sip in siplist:
  ipchecking = checkipadd.check_ips(sip)                          #Module to check given ip is Address or Network
  if str(ipchecking) == "<class 'ipaddress.IPv4Address'>":       #condition if given string is ip address
       siptype.append("Address")
       sip_name="H-"+sip                              #Standardized Name prefix
       sip_name_list.append(sip_name)                            #it will update list of single ips into dictionaries
  elif str(ipchecking) == "<class 'ipaddress.IPv4Network'>":     #same for subnets
       siptype.append("Network")
       sourceip=sip.split('/')[0]
       sip_mask=sip.split('/')[1]
       sip_name="N-"+sourceip+"_"+sip_mask
       sip_name_list.append(sip_name)
#print("SIP_Name_List: ",sip_name_list)
url_name=""
url_list=[]
for dip in diplist:
    ipchecking = checkipadd.check_ips(dip)
    if str(ipchecking) == "<class 'ipaddress.IPv4Address'>":       #condition if given string is ip address
       diptype.append("Address")                              #it will update list of single ips into dictionaries
       dip_name="H-"+dip
       dip_name_list.append(dip_name)
    elif str(ipchecking) == "<class 'ipaddress.IPv4Network'>":     #same for subnets
       diptype.append("Network")
       destip=dip.split('/')[0]
       dip_mask=dip.split('/')[1]
       dip_name="N-"+destip+"_"+dip_mask
       dip_name_list.append(dip_name)
    elif isinstance(dip.split(".")[-1],str)==True:              #It will check if value given is string to define URL
      #print("URL trigger for ",dip)
      raw=dip.replace(' ',',')
      raw=dip.replace(';',',')
      raw_split=raw.split(',')
      list_url=str(raw_split[0])
      urlvalue=len(list_url)
      url_name=rulename+"-url"
      for url in raw_split:
        diptype.append("URL")
        url_list.append(url_name)
        with contextlib.redirect_stdout(None):
          p.create_custom_url(url_name,url,device_group)            #Create URL Object
    else:
       print("Wrong Input in Destination Field.")
#print("DIP_name_list: ",dip_name_list)
#print("DIP type: ",diptype,url_name)
#print("URL LIst: ",url_list)

##***************Zone Declaration**********************##
trust_network_range=[]                                            #List of Trust Network range provided by Network Team
trust_network_range.append(ipaddress.ip_network('Add your IPrange of trust zone'))
trust_network_range.append(ipaddress.ip_network('Add your IPrange of trust zone'))
trust_network_range.append(ipaddress.ip_network('Add your IPrange of trust zone'))

for sip in siplist:
    ip_from_user=ipaddress.ip_network(str(sip))
    if ip_from_user in trust_network_range[0] or ip_from_user in trust_network_range[1] or ip_from_user in trust_network_range[2] or ip_from_user.overlaps(trust_network_range[0]) or ip_from_user.overlaps(trust_network_range[1]) or ip_from_user.overlaps(trust_network_range[2]):
        zsiplist.append("trust")              #it will append zone detials to dictionary
    else:
        zsiplist.append("untrust")
for dip in diplist:
  if "URL" in diptype:
    zdiplist.append("untrust")
  else:
    ip_from_user=ipaddress.ip_network(str(dip))
    if ip_from_user in trust_network_range[0] or ip_from_user in trust_network_range[1] or ip_from_user in trust_network_range[2] or ip_from_user.overlaps(trust_network_range[0]) or ip_from_user.overlaps(trust_network_range[1]) or ip_from_user.overlaps(trust_network_range[2]):
      zdiplist.append("trust")
    else:
      zdiplist.append("untrust")

scounttrust = zsiplist.count("trust")
scountuntrust = zsiplist.count("untrust")
dcounttrust = zdiplist.count("trust")
dcountuntrust = zdiplist.count("untrust")

##it will define trust/untrust zone details for each ip
if (scounttrust == len(zsiplist)) and (dcounttrust == len(zdiplist)):
   #print("all sip trust and dip trust")
   t1= "trust"
   t2= "trust"
   t3= "trust"
   t4= "trust"
elif (scountuntrust == len(zsiplist)) and (dcountuntrust == len(zdiplist)):
     #print("all sip untrust and dip untrust")
     t1 = "untrust"
     t2 = "untrust"
     t3 = "untrust"
     t4 = "untrust"
elif (scounttrust == len(zsiplist)) and (dcountuntrust == len(zdiplist)):
     #print("all sip trust and dip untrust")
     t1 = "trust"
     t2 = "trust"
     t3 = "untrust"
     t4 = "untrust"
elif (scountuntrust == len(zsiplist)) and (dcounttrust == len(zdiplist)):
     #print("all sip untrust and dip trust")
     t1 = "untrust"
     t2 = "untrust"
     t3 = "trust"
     t4 = "trust"
elif (scounttrust != len(zsiplist)) and (scountuntrust != len(zsiplist)) and (dcountuntrust == len(zdiplist)):
     t1 = "trust"
     t2 = "untrust"
     t3 = "untrust"
     t4 = "untrust"
elif (scounttrust != len(zsiplist)) and (scountuntrust != len(zsiplist)) and (dcounttrust == len(zdiplist)):
     t1 = "trust"
     t2 = "untrust"
     t3 = "trust"
     t4 = "trust"
elif (dcounttrust != len(zdiplist)) and (dcountuntrust != len(zdiplist)) and (scounttrust == len(zsiplist)):
     t1 = "trust"
     t2 = "trust"
     t3 = "trust"
     t4 = "untrust"
elif (dcounttrust != len(zdiplist)) and (dcountuntrust != len(zdiplist)) and (scountuntrust == len(zsiplist)):
     t1 = "untrust"
     t2 = "untrust"
     t3 = "trust"
     t4 = "untrust"
elif ((scounttrust != len(zsiplist)) and (scountuntrust != len(zsiplist))) and ((dcounttrust != len(zdiplist)) and (dcountuntrust != len(zdiplist))):
     t1 = "trust"
     t2 = "untrust"
     t3 = "trust"
     t4 = "untrust"
else:
  pass
#print("Zone values for each Ip: ",t1,t2,t3,t4)

##****************Routecheck And Call To RouteCreation********##
ipcount = sipcount+dipcount
iptype = siptype+diptype
i=0
for ip in iplist:
  if i < ipcount:
    if iptype[i] == "Address":
      with contextlib.redirect_stdout(None):
        routecheck.main_ip(ip,rulename)                       #it will create Route in PA FW
    elif iptype[i] == "Network":
      with contextlib.redirect_stdout(None):
        routecheck.main_ipnet(ip,rulename)
    else:
      pass
  i=i+1
#time.sleep(5)

##**********Address Object Check and Creation**************##
for sip in siplist:
    ip_exist = p.address(sip,device_group)
    ip_existlist.append(ip_exist)
    if int(ip_exist) == 0:
      p.create_address(sip,device_group)                                #It will create Source IP Object
    else:
      pass

for dip in diplist:
  ind=diplist.index(dip)
  if diptype[ind]=="Address":
    ip_exist = p.address(dip,device_group)
    ip_existlist.append(ip_exist)
    if int(ip_exist) == 0:
      p.create_address(dip,device_group)                             #It will create Dest IP Object
    else:
      pass
  elif diptype[ind]=="Network":
    ip_exist = p.check_subnet(dip,device_group)
    ip_existlist.append(ip_exist)
    if int(ip_exist) == 0:
      p.create_subnet(dip,device_group)
    else:
      pass
  else:
    pass
#print("IP exist status: ",ip_existlist)

##************Service Object Check and Creation**************##
for port in serviceportlist:
  service_name= serviceprotocol+"-"+port
  service_name_list.append(service_name)
  service_status = p.service(service_name,device_group)
  if int(service_status) == 0:
    p.create_service(service_name,serviceprotocol,port,device_group)             #it will created Service Object
  else:
    pass

##*****************Schedule Object check And Create*************##
scheduler_name = rulename+"-"+datetime.datetime.today().strftime('%d-%m-%Y')
start_date = datetime.datetime.today().strftime('%Y/%m/%d')
next_date = (datetime.datetime.today() + datetime.timedelta(days=int(number_days))).strftime('%Y/%m/%d')
#print("Dates: ",scheduler_name,start_date,next_date)
if int(number_days) == 0:
  Temp = False
elif int(number_days) > 0:
  Temp = True
  p.create_schedule(scheduler_name,start_date,next_date,device_group)                 #It will create Schedule Object
else:
  print("Issue in Schedule Object.")
  pass

##*****************Rule Creation*************##
if Temp == True:
  for sip in sip_name_list:
    if "URL" in diptype:
      with contextlib.redirect_stdout(None):
        prerule.create_url_whitelist_tmp(rulename,sip,description,t1,t2,url_name,scheduler_name,device_group)            #It will create Temp Whitelisting
    else:
      for dip in dip_name_list:
        for service_name in service_name_list:
          with contextlib.redirect_stdout(None):
            prerule.create_port_open_prerule_tmp(rulename,sip,dip,service_name,description,t1,t2,t3,t4,scheduler_name,device_group)   #Temp rule Create
            #print(rulename,sip,dip,service_name,description,t1,t2,t3,t4,device_group,scheduler_name)

elif Temp == False:
  for sip in sip_name_list:
    if "URL" in diptype:
      prerule.create_url_whitelist(rulename,sip,description,t1,t2,url_name,device_group)           #It will create permanent URL whitelisting
    else:
      for dip in dip_name_list:
        for service_name in service_name_list:
          with contextlib.redirect_stdout(None):
            #print("Permanent Rule Triggered")
            prerule.create_port_open_prerule(rulename,sip,dip,service_name,description,t1,t2,t3,t4,device_group)    #Permanent Rule create
            #print(rulename,sip,dip,service_name,description,t1,t2,t3,t4,device_group,number_days)

##**************Commit Changes**************##
def commitchanges():
###To commit changes on Panorama
    p = panobjects.panorama_objects()                         #It will commit all changes to panaroma
    commit_jobid = p.commits()
    print("commit job id for panaroma is"+" "+ commit_jobid)
    commit_jobstatus = p.commits()
    print(commit_jobstatus)

def commitchanges_device():
###To commit changes on Palalto device
    p = panobjects.panorama_objects()                             #it will commit all changes to palo alto
    commit_device_jobid = p.commits_device()   
    print("commit job id for device is"+" "+ commit_device_jobid)
    #commit_device_jobstatus = p.commits_device()
    #print(commit_device_jobstatus)

commitchanges()         #call to commit to panaroma

##********check rule created or not on panaroma***###
prerule = create_pre_rule_ver2.panorama_prerule()
rulepresent = prerule.checkrulepresent(rulename,device_group)          #it will check if rule is present or not
if rulepresent == "1":
    print("DMZ port opening rule created successfully on Panaroma.")
else:
    print("Rule is not showing on Panaroma")

##***********Push changes to firewall**************###
#time.sleep(20)
commitchanges_device()          #call given to module to push changes to device

##*************Check rule created or not on device*********##
#time.sleep(60)
#rulepresent = prerule.checkdevicerulepresent(rulename,device_group)          #it will check if rule is present or not
#if rulepresent == "1":
#    print("DMZ port opening rule created successfully on Device.")
#else:
#    print("Rule is not showing on Device")
#########################################################################
