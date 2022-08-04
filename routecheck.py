##############################
#Scripted in Python
#Script to Check given ip/network is already present in routes or not
##############################

import pandas as pd						#liabrary to read csv file
import paloalto                                                 #custom liabrary to call module to create route
import ipaddress						#liabrary to convert string to ipaddress format
import sys

class routecheck:                                               #Class created for routecheck
      def main_ip(*args):                                       #function created to call later
         input_raw = args[0]                                    #ip details fetched from main inputs
         rulename = args[1]
         first_col = pd.read_csv("<path/fileCotainsRouteDump>", usecols = [0])     #present ip routes fetched from dump
         ip_list = first_col.values.tolist()                    #converted values of columns to list to be perform
         a = []
         try:
            ipadd = ipaddress.ip_address(input_raw)             #raw string input converted to ip address format
            for i in ip_list:                                   #it will itterate to all networks from list of networks
                ip_net = ipaddress.ip_network(i[0])             #first will convert network from string format to netwrok format
                if ipadd in ip_net:                             #condition to check given ip address is present in ip network list
                   a.append(1)                                  #it will return 1 if present and 0 if not to the "a" list
                else:
                   a.append(0)
         except ValueError as err:                              #same it will convert and check for user given networks
             try:
                ipnet = ipaddress.ip_network(input_raw)
                for i in ip_list:
                    ip_net = ipaddress.ip_network(i[0])
                    if ipnet == ip_net:
                       a.append(1)
                    elif ipnet.overlaps(ip_net)== True:
                         a.append(1)
             except:
                print("Enter Valid IP Address/Network.")
                #wrong_input()	
         if all([ v == 0 for v in a ]) :                             #at the end of the loop it will check for "a" variable if all values are 0
            print("Route Creating...")                                    #0 means ip is not present in route, it will call module to create route.
            
            paloalto.paloalto_objects.create_route_ip(rulename,input_raw)     #call given to create ip route
            commit_jobid = paloalto.paloalto_objects.commits_paloalto()       #commit id and status will be fetched and print to console
            print("commit job id is"+" "+ commit_jobid)
            commit_jobstatus = paloalto.paloalto_objects.commits_paloalto()
            print(commit_jobstatus)
            
         elif any([ v == 1 for v in a ]):                             #if we get any 1 in "a" list, it means we have given ip already in networks present
              print("Route Already present!!!")
         else:
             pass
             print("Route Already present!!!")

      def main_ipnet(*args):
         input_raw = args[0]
         rulename = args[1]
         first_col = pd.read_csv("<path/fileCotainsRouteDump>", usecols = [0])		
         ip_list = first_col.values.tolist()
         a = []
         try:
            ipadd = ipaddress.ip_address(input_raw)
            for i in ip_list:
                ip_net = ipaddress.ip_network(i[0])
                if ipadd in ip_net:
                   a.append(1)
                else:
                   a.append(0)
         except ValueError as err:
             try:
                ipnet = ipaddress.ip_network(input_raw)
                for i in ip_list:
                    ip_net = ipaddress.ip_network(i[0])
                    if ipnet == ip_net:
                       a.append(1)
                    elif ipnet.overlaps(ip_net)== True:
                         a.append(1)
             except:
                print("Enter Valid IP Address/Network.")
                #wrong_input()	

##it will check for all IPs and give result.
         if all([ v == 0 for v in a ]) :
            print("Creating Route")
            
            paloalto.paloalto_objects.create_route_subnetip(rulename,input_raw)
            commit_jobid = paloalto.paloalto_objects.commits_paloalto()
            print("commit job id is"+" "+ commit_jobid)
            commit_jobstatus = paloalto.paloalto_objects.commits_paloalto()
            print(commit_jobstatus)
            
         elif any([ v == 1 for v in a ]):
              print("Route Already present!!!")
         else:
             pass
             print("Route Already present!!!")
