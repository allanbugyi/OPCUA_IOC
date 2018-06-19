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
import numpy as np

from pkg_resources import require
require('cothread==2.14')
require('epicsdbbuilder==development')

# Import basic DLS softIoc framework
from softioc import softioc, builder, device

#FreeOpcUa python package
from opcua import Client, ua, common

#Set IOC's name
builder.SetDeviceName('CP_HVAC')

# ------- Automated PV generation from OPC UA XML schema -------

#Extracting only the nodes, which means all the <UAVariable> items
nodeExtraction_xml = subprocess.check_output(['sed', '-n', '/^<UAVariable.*BrowseName=".*".*ParentNodeId="ns=.*;s=.*".*DataType=".*"/p', argv[1]])
#Some variable initialization
pvs_To_NodesOPCUA_mapping = {}

#Extracting NodeId, BrowseName, ParentNodeId, DataType, AccessLevel from the selected lines
for line in nodeExtraction_xml.splitlines():
	#Some pre-processing due to Siemens PLC broken XML
	newline = line.replace('&quot;', '"') 
	
	left_tag_exclusion = newline[20:]
	split_on_whitespaces = left_tag_exclusion.split(" ")

	#Extracting NodeId
	nodeId = split_on_whitespaces[0]
	#print nodeId
	if((nodeId[((len(nodeId))-1)] == '"') and  (nodeId[((len(nodeId))-2)] == '"')): 
		nodeId = nodeId[:-1]
	else: 
		nodeId = nodeId.rstrip('"')
	#print nodeId
	#Extracting BrowseName
	browseName = split_on_whitespaces[1].replace('BrowseName="', "")
	browseName = browseName.rstrip('"')
	#Extracting ParentNodeId
	parentNodeId = split_on_whitespaces[2].replace('ParentNodeId="', "")
	parentNodeId = parentNodeId.rstrip('"')
	
	parentNodeId_test = ""
	if ((len(parentNodeId) > 8)):
		if (parentNodeId[7] != '"'):
			parentNodeId_test = parentNodeId[7:]
		else:
			parentNodeId_test = parentNodeId[8:]
		
	#Deciding whether all the PV creation should continue based on the ParentNode. This avoids the creation of unecessary PVs (or actually, PVs that 
	#reference not desired Nodes (e.g., Nodes without attributes), which are without any use to EPICS)
	if((parentNodeId_test == "Inputs") or (parentNodeId_test == "Outputs") or (parentNodeId_test == "HMI") or (parentNodeId_test == "PID_memories")):#The ParentNodes which hold PVs
		#Continues extracting properties from XML ...		
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
		
		#The PV's finals name for inside python referencing
		pvName = "pv_" + parentNodeId_test + "_" + browseName[2:]#Notice that for python softIoc we use the convention '_' instead of EPICS' separator ':', 
									 #which is a special character for Python
		#Decision making based on which datatype PV will be set
		if 	(dataType == 'bool' or dataType == 'BOOL'): 
				nodeOPCUA_properties_list = [nodeId, browseName, parentNodeId, dataType, accessLevel]
				#PV creation
				pvItself = builder.boolIn((parentNodeId_test+browseName[1:]))#PV's name fiting EPICS convention, with the ':' separating PVs' names, so 'caget' works fine
				linkInformation_array = [nodeOPCUA_properties_list, pvItself]
				pvs_To_NodesOPCUA_mapping.update({pvName: linkInformation_array})
		elif	(dataType == "Int16" or dataType == "INT" or dataType == "UInt16" or dataType == "UINT" or dataType == "Int32" 
			or dataType == "UInt32" or dataType == "UDINT"):				
				nodeOPCUA_properties_list = [nodeId, browseName, parentNodeId, dataType, accessLevel]
				#PV creation
				pvItself = builder.longIn((parentNodeId_test+browseName[1:]))#PV's name fiting EPICS convention, with the ':' separating PVs' names,so 'caget' works fine 
				linkInformation_array = [nodeOPCUA_properties_list, pvItself]
				pvs_To_NodesOPCUA_mapping.update({pvName: linkInformation_array})	
	else:	
		continue
		
# ---------------------------------------------------------

#Create OPCUA client using the OPC UA server's 'IP:port' address
if(argv[2]==""):
	client = Client("opc.tcp://10.2.121.202:4840")
else:
	client = Client("opc.tcp://" + argv[2])
 
try:
	#Establish connection with OPC UA Server
	client.connect()

	#function for monitoring the specified INPUT PV, equivalent to camonitor Channel Access command
	def monitorPV (pv_name, scan_period):
		arrayMappedPV = pvs_To_NodesOPCUA_mapping[pv_name]
		nodeOPCUA_properties_list = arrayMappedPV[0]
		nodeId = nodeOPCUA_properties_list[0]	
		handler = SubHandler()
        	sub = opcua_server.create_subscription(500, handler)
		node = client.get_node(nodeId)
        	handle = sub.subscribe_data_change(node)		
		'''
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
		'''

	#readPV and writePV: functions to read and write to specific PVs, equivalent to caget and caput Channel Access commands
	
	def readPV (pv):
		'''
		#preparing string equivalent to BrowseName field format from the Node (which represents the PV) in OPC UA Server address space
		pv_name_str = pv.name 				#storing the pv's complete name 
		record_name = pv_name_str[8:]			#removing the Device prefix from the pv's name
		opcua_node_browseName = "3:"+record_name 	#adding the level found in OPC UA server's address space (in this case 3) and setting the BrowseName 
		opcua_childNode_pv = parentNode_OUTPUT_PVs.get_child(opcua_node_browseName)
		(pv).set(int (opcua_childNode_pv.get_value()))
		print((pv.name) + "\t" + str((pv).get()))
		'''
	def writePV (pv_name, value):
		arrayMappedPV = pvs_To_NodesOPCUA_mapping[pv_name]
		nodeOPCUA_properties_list = arrayMappedPV[0]
		pv = arrayMappedPV[1]
		nodeId = nodeOPCUA_properties_list[0]
		dataType = nodeOPCUA_properties_list[3]
		opcua_node_pv = client.get_node(nodeId)
		var = ua.Variant(value, (opcua_node_pv.get_data_type_as_variant_type()))
		
		print((pv.name) + "\tOld value: " + str((pv).get()))
		opcua_node_pv.set_value(var)
		pv.set(opcua_node_pv.get_value())	
		print((pv.name) + "\tNew value: " + str((pv).get()))

	# Run the IOC.  This is boilerplate, and must always be done in this order,
	# and must always be done after creating all PVs.
	builder.LoadDatabase()
	softioc.iocInit()
	
	softioc.interactive_ioc(globals())
finally:
	client.disconnect()




