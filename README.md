# PaloAltoPortOpeningAutomation
This is Automation Project to Automate task of Creating Port Opening Rule On Panaroma and then push to Palo Alto device once user log request with required parameter.

Flow:
1. User will log ticket on ticketing tool.
2. After all approvals it will hit Orchastration tool.
3. Orchastration tool will trigger AutomationVer2.py script with all required details.
4. Script will first check all parameters are valid or not.
5. Then it will check for all objects are created or not. If not present it will call API to Create respective Object(ex. Address, Schedule Object).
6. It will check for routes. if not present it will create route for given IPs.
7. Finally it will call API to create Rule on Panaroma and then push it on Palo Alto Device.
8. Script will give success status to Orchestration and finally forwarded it to the ticketing tool.

File Description:
1. final.py		This is main script which will run from orchestration.
2. multipleinput.py	First all arguments will be handled in this script.
3. panobjects.py		This script will be triggered to check all required objects are present or not.
4. create_pre_rule.py	This script is to create final rule once we meet all prerequisite.
5. paloalto.py		This script is to commit rule to device and create routes
6. checkipadd.py		This script is to convert given string input to IP format and validate
7. routecheck.py		This script is to check given IP is already present in list. if not it will create IP Route.
8. AutomationVer2.py			This script is Version 2 of Our Projects simplified by OK.
9. config.py		This is secret file do not touch it.
10. create_pre_rule_ver2.py This is version2 of Prerule create file in simplified manner by OK.

Other Files:
dump.csv		This is dump of all routes present.
input_parameter.txt	All input parameters stored in this file.
ipdetails.csv		sIP and dIP combination is created to be used in script.
zone.csv		zone for each IP stored in this file.
basic_query		bais querie for testing purpose(Input parameter).
input_parameter.txt	This will append all Input parameteres

Extra files created for testing only
testing.py
test.py
final22022022.py
create_pre_rule.pyc
panobjects.pyc
