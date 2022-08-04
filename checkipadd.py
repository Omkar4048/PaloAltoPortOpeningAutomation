##############################
###
#Scripted by OK
#Language Python
#Script to Check Given Raw Input by User is Single IP or IP Network 
###
##############################

import ipaddress       #importing module to change type to ipaddress or network
import sys             #importing module to use system arguments

        
def check_ips(Var):                    #Function creation to check IP address
    global ipadd                       #Defined global variable to check
    global ipcheck
    
    try:                              #we used try except block to avoid error after we enter network into IP field
       ipadd = ipaddress.ip_address(Var)             #it will convert type of variable into IP address format
       #print(type(ipadd))
       ipcheck = type(ipadd)
       return ipcheck
    except ValueError as err:         #if user enters network as input it will throw error in try block and excpt block will handle this
       try:
          ipadd = ipaddress.ip_network(Var)      #it will convert type of variable into IP network format
          ipcheck = type(ipadd)
          return ipcheck
       except:
          print("Invalid Input.")            #for wrong format it will print invalid input
          #pass

#check_ip()                  #to call defined function
#i=checkipadd()
#i.check_ip()
