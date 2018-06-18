# -*- coding: utf8 -*-
######################################################################################################################################
#	EPICS IOC developed with DLS Softioc Framework with support for OPC UA communication based on FreeOpcUa python package       #
#	Brazilian Synchroton Light Laboratory - Campinas, 06/xx/2018								     #
#	Author: Allan Serra Braga Bugyi	(allan.bugyi@lnls.br)									     #
#	In response to Ocommon's occurrence: 6134										     #
#	Version: 1.0														     #
#	Tested  - Siemens PLC S7-1500										     		     #
######################################################################################################################################

import time
import subprocess
from sys import argv

from pkg_resources import require
require('cothread==2.14')
require('epicsdbbuilder==development')

# Import basic DLS softIoc framework
from softioc import softioc, builder, device

#FreeOpcUa python package
from opcua import Client, ua

#Set IOC's name
builder.SetDeviceName('CP_HVAC')

#Automated PV generation from OPC UA XML schema

#Extracting only the nodes, which means all the <UAVariable> items
nodeExtraction_xml = subprocess.check_output(['sed', '-n', '/^<UAVariable.*BrowseName=".*".*ParentNodeId="ns=.*;s=.*".*DataType=".*"/p', argv[1]])
#Some variable initialization
pvs_To_NodesOPCUA_mapping = {}

#Extracting NodeId, BrowseName, ParentNodeId, DataType, AccessLevel from the selected lines
for line in nodeExtraction_xml.splitlines():
	#Some pre-processing due to Siemens PLC broken XML
	newline = line.replace('&quot;', "") 
	
	left_tag_exclusion = newline[20:]
	split_on_whitespaces = left_tag_exclusion.split(" ")

	#Extracting NodeId
	nodeId = split_on_whitespaces[0].rstrip('"')
	#Extracting BrowseName
	browseName = split_on_whitespaces[1].replace('BrowseName="', "")
	browseName = browseName.rstrip('"')
	#Extracting ParentNodeId
	parentNodeId = split_on_whitespaces[2].replace('ParentNodeId="', "")
	parentNodeId = parentNodeId.rstrip('"')
	
	#Deciding whether all the PV creation should continue based on the parent Node. This avoids the creation of unecessary PVs
	parentNodeId_test = parentNodeId[7:]
	if((parentNodeId_test == "Inputs") or (parentNodeId_test == "Outputs") or (parentNodeId_test == "HMI") or (parentNodeId_test == "PID_memories")):
		# continues extracting properties from XML ...		
		#Extracting DataType	
		dataType = split_on_whitespaces[3].replace('DataType="', "")
		dataType = dataType.rstrip('"')
		dataType = dataType.rstrip('">')
		#Extracting AccessLevel
		accessLevel = ""
		if (len(split_on_whitespaces) > 4):
			accessLevel = split_on_whitespaces[4].replace('AccessLevel="', "")
			accessLevel = accessLevel.rstrip('"')
			accessLevel = accessLevel.rstrip('">')
		'''
		#Checks if the PV's name is not already defined (Note: It was defined as a convention that EPICS PVs' names have the 'pv_'preffix)
		test = "pv_" + parentNodeId[7:] + "_" + browseName[2:] #Notice that for python softIoc we use the convention '_' instead of EPICS' separator ':', 
								       #which is a special character for Python
		if(test in pvs_To_NodesOPCUA_mapping):
			counter = 2
			test = test + "-"		
			while True:
				test = test + str(counter)		
				if(test in pvs_To_NodesOPCUA_mapping):
					test = test.rstrip((str(counter)))
					counter += 1
				elif(test not in pvs_To_NodesOPCUA_mapping): 
					#If it's already defined, it creates a unique suffix accordingly (like '_2'for the second time the PV's name appear, 
					#'_3' for the third time, and so on)
					browseName = test.replace("pv_", "")
					break
		'''
		#The PV's finals name
		pvName = "pv_" + parentNodeId[7:] + "_" + browseName[2:]

		#Decision making based on which datatype PV will be set
		if 	(dataType == 'bool' or dataType == 'BOOL'): 
				nodeOPCUA_properties_list = [nodeId, browseName, parentNodeId, dataType, accessLevel]
				#PV creation
				pvItself = builder.boolIn((parentNodeId[7:]+browseName[1:]))
				linkInformation_array = [nodeOPCUA_properties_list, pvItself]
				pvs_To_NodesOPCUA_mapping.update({pvName: linkInformation_array})
		elif	(dataType == "Int16" or dataType == "INT" or dataType == "UInt16" or dataType == "UINT" or dataType == "Int32" 
			or dataType == "UInt32" or dataType == "UDINT"):				
				nodeOPCUA_properties_list = [nodeId, browseName, parentNodeId, dataType, accessLevel]
				#PV creation
				pvItself = builder.longIn((parentNodeId[7:]+browseName[1:])) 
				linkInformation_array = [nodeOPCUA_properties_list, pvItself]
				pvs_To_NodesOPCUA_mapping.update({pvName: linkInformation_array})	
	else:	
		continue
		

#Create OPCUA client
client = Client("opc.tcp://10.2.121.202:4840")
 
try:
	#Establish connection with OPC UA Server
	client.connect()
	
	#OPC UA parent Node from 'INPUT' PVs
	parentNode_INPUT_PVs 	= client.get_node("ns=3;s=Inputs")
     
	#OPC UA parent Node from 'OUTPUT' PVs
	parentNode_OUTPUT_PVs	= client.get_node("ns=3;s=Outputs")

	
	#specific OPC UA parent Nodes from Siemens S7-1500
	#OPC UA parent Node from 'HMI' PVs
	parentNode_HMI_PVs 		= client.get_node("ns=3;s=PID_memories")
	#OPC UA parent Node from 'PID_memories' PVs
	parentNode_PID_memories_PVs 	= client.get_node("ns=3;s=HMI")
	
	#function for monitoring the specified INPUT PV, equivalent to camonitor Channel Access command
	def monitorPV (scan_period, pv):	
		#preparing string equivalent to BrowseName field format from the Node (which represents the PV) in OPC UA Server address space
		pv_name_str = pv.name 				#storing the pv's complete name 
		record_name = pv_name_str[8:]			#removing the Device prefix from the pv's name
		opcua_node_browseName = "3:"+record_name 	#adding the level found in OPC UA server's address space (in this case 3) and setting the BrowseName 
		#executes till user terminates		
		try:		
			while True:
				opcua_childNode_pv = parentNode_INPUT_PVs.get_child(opcua_node_browseName)
				(pv).set(int (opcua_childNode_pv.get_value()))
				print((pv.name) + "\t" + str((pv).get()))
				time.sleep(scan_period)	
		except KeyboardInterrupt, e:
			print "\n- Stopped Monitoring -"
	

	#readPV and writePV: functions to read and write to specific PVs, equivalent to caget and caput Channel Access commands
	
	def readPV (pv):
		#preparing string equivalent to BrowseName field format from the Node (which represents the PV) in OPC UA Server address space
		pv_name_str = pv.name 				#storing the pv's complete name 
		record_name = pv_name_str[8:]			#removing the Device prefix from the pv's name
		opcua_node_browseName = "3:"+record_name 	#adding the level found in OPC UA server's address space (in this case 3) and setting the BrowseName 
		opcua_childNode_pv = parentNode_OUTPUT_PVs.get_child(opcua_node_browseName)
		(pv).set(int (opcua_childNode_pv.get_value()))
		print((pv.name) + "\t" + str((pv).get()))

	def writePV (pv, value):
		#preparing string equivalent to BrowseName field format from the Node (which represents the PV) in OPC UA Server address space
		pv_name_str = pv.name 				#storing the pv's complete name 
		record_name = pv_name_str[8:]			#removing the Device prefix from the pv's name
		opcua_node_browseName = "3:"+record_name 	#adding the level found in OPC UA server's address space (in this case 3) and setting the BrowseName 
		opcua_childNode_pv = parentNode_OUTPUT_PVs.get_child(opcua_node_browseName)
		(pv).set(int (opcua_childNode_pv.get_value()))
		print((pv.name) + "\tOld value: " + str((pv).get()))
		opcua_childNode_pv.set_value(value)
		(pv).set(int (opcua_childNode_pv.get_value()))
		print((pv.name) + "\tNew value: " + str((pv).get()))	


	# Run the IOC.  This is boilerplate, and must always be done in this order,
	# and must always be done after creating all PVs.
	builder.LoadDatabase()
	softioc.iocInit()
	
	softioc.interactive_ioc(globals())
finally:
	client.disconnect()




