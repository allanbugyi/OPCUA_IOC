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
nodeExtraction_xml = subprocess.check_output(['sed', '-n', '/^<UAVariable.*BrowseName=".*"*ParentNodeId="ns=.*;s=.*".*DataType=".*"/p', argv[1]])
#Extracting NodeId, BrowseName, ParentNodeId, DataType, AccessLevel
for line in nodeExtraction_xml.splitlines():
	#Some pre-processing due to Siemens PLC broken XML
	newline = line.replace('&quot;', "") 
	left_junk_exclusion = newline[20:]
	split_on_whitespaces = left_junk_exclusion.split(" ")

	#Extracting NodeId
	nodeId_value = split_on_whitespaces[0].rstrip('"')
	#Extracting BrowseName
	browseName = split_on_whitespaces[1].replace('BrowseName="', "")
	browseName = browseName.rstrip('"')
	#Extracting ParentNodeId
	parentNodeId = split_on_whitespaces[2].replace('ParentNodeId="', "")
	parentNodeId = parentNodeId.rstrip('"')
	#Extracting DataType	
	dataType = split_on_whitespaces[3].replace('DataType="', "")
	dataType = dataType.rstrip('"')
	dataType = dataType.rstrip('">')
	

#Create INPUT PVs
pv_23B18            = builder.longIn("23B18")		#Temperatura precisão Aquecedor Fino
pv_23B19            = builder.longIn("23B19")		#Temperatura Ambiente 1
pv_23B20            = builder.longIn("23B20")		#Temperatura Ambiente 2
pv_23B21            = builder.longIn("23B21")		#Temperatura Ambiente 3
pv_23B22            = builder.longIn("23B22")		#Temperatura Ambiente 4
pv_23B23            = builder.longIn("23B23")		#Pressão Ambiente
pv_23B24_H          = builder.longIn("23B24_H")		#Umidade Aquecedor Fino
pv_23B24_T          = builder.longIn("23B24_T")		#Temperatura Aquecedor Fino
pv_CP_23B10         = builder.longIn("CP-23B10")	#Temperatura Agua entrada
pv_CP_23B11         = builder.longIn("CP-23B11")	#Temperatura Agua Retorno
pv_CP_23B13         = builder.longIn("CP-23B13")	#Temperatura precisão Ar Externo
pv_CP_23B14_H       = builder.longIn("CP-23B14_H")	#Umidade Ar externo
pv_CP_23B14_T       = builder.longIn("CP-23B14_T")	#Temperatura Ar externo
pv_CP_23B15         = builder.longIn("CP-23B15")	#Temperatura precisão Retorno
pv_CP_23B16_H       = builder.longIn("CP-23B16_H")	#Umidade Retorno
pv_CP_23B16_T       = builder.longIn("CP-23B16_T")	#Temperatura Retorno
pv_CP_23B17         = builder.longIn("CP-23B17")	#Temperatura precisão Aquecedor Grosseiro
pv_CP_23B25_H       = builder.longIn("CP-23B25_H")	#Umidade Serpentina
pv_CP_23B25_T       = builder.longIn("CP-23B25_T") 	#Temperatura Serpentina
pv_CP_23B26         = builder.longIn("CP-23B26")	#Temperatura Precisão Serpentina
pv_CP_23B27         = builder.boolIn("CP-23B27")	#Estado Termostato AQ1
pv_CP_23B28         = builder.longIn("CP-23B28")	#Temperatura precisão Aquecedor Fino
pv_CP_23B29         = builder.boolIn("CP-23B29")	#Estado Pressostato FC1
pv_CP_23B30         = builder.longIn("CP-23B30")	#Pressão Filtro Fino
pv_CP_23B31         = builder.longIn("CP-23B31")	#Pressão Filtro Grosso
pv_CP_23M10_RET     = builder.longIn("CP-23M10_RET")	#Retorno Dumper FCV152
pv_CP_23M7_RET      = builder.longIn("CP-23M7_RET")	#Retorno Dumper FCV150
pv_CP_23M8_RET      = builder.longIn("CP-23M8_RET")	#Retorno Dumper FCV151
pv_CP_23M9_FDB_Hz   = builder.longIn("P-23M9_FDB_Hz")	#FeedBackV20
pv_CP_23M9_Status   = builder.boolIn("CP-23M9_Status") 	#Estado Inversor V20 FC1 - FCT140
pv_CP_23X1_RET      = builder.longIn("CP-23X1_RET")	#Retorno Atuador Valvula
pv_Emergencia_Gases = builder.boolIn("Emergencia_Gases", ZNAM=False, ONAM=True)
#pv_PrimaxP_Alm_RL_NC= builder.xxxxIn("")
#pv_PrimaxP_Alm_RL_NO= builder.xxxxlIn("")
#pv_PrimaxP_Flr_RL_NC= builder.xxxxIn("")
#pv_PrimaxP_Flr_RL_NO= builder.xxxxIn("")
#pv_PrimaxP_VOL_O2   = builder.xxxxIn("")
pv_StatusContatorAQ1	= builder.boolIn("StatusContatorAQ1", ZNAM=False, ONAM=True) #Estado Contator AQ1
pv_StatusContatorAQ1_1A = builder.boolIn("StatusContatorAQ1-1A", ZNAM=False, ONAM=True) #Estado Contator AQ1.1A
pv_StatusDisjuntorMotor1 = builder.boolIn("StatusDisjuntorMotor1", ZNAM=False, ONAM=True) #Estado Disjuntor Motor 1

#Create OUTPUT PVs
pv_AQ_Reserve		= builder.longOut("AQ_Reserve")		#Inverosr (2)
pv_CP_PLUS_CP_23W3	= builder.longOut("CP_+_CP-23W3")	#Aquecedor Grosso
pv_CP_23M10		= builder.longOut("CP-23M10")		#Damper 3 Insulflamento - FCV152
pv_CP_23M12		= builder.boolOut("CP-23M12")		#Damper 4 Exaustão - FCV154
pv_CP_23M7		= builder.longOut("CP-23M7")		#Damper 1 Retorno - FCV150
pv_CP_23M8		= builder.longOut("CP-23M8")		#Damper 2 TAE - FCV151
pv_CP_23M9_ACK		= builder.boolOut("CP-23M9_ACK")	#V20 FC1 DI3 - ACK Falha
pv_CP_23M9_Freq_Hz	= builder.longOut("CP-23M9_Freq_Hz")	#Inversor V20 - Frequencia em Hz
pv_CP_23M9_Jog		= builder.boolOut("CP-23M9_Jog")	#V20 FC1 DI4 - Jog a Frente
pv_CP_23M9_On_Off	= builder.boolOut("CP-23M9_On/Off")	#V20 FC1 DI1 - On/Off
pv_CP_23M9_Reverso	= builder.boolOut("CP-23M9_Reverso")	#V20 FC1 DI2 - Reverso
pv_CP_23W2		= builder.longOut("CP-23W2")		#Aquecedor Fino
pv_CP_23X1		= builder.longOut("CP-23X1")		#Valvula Agua Gelada
pv_DQ_RESERVE1		= builder.boolOut("DQ_RESERVE1")	#RESERVE 1
pv_DQ_RESERVE2		= builder.boolOut("DQ_RESERVE2")	#RESERVE 2
pv_ResetSecuritySystem	= builder.boolOut("Reset_Security_System")#Reset Security System

#lists of PVs grouped by category
inputPVs_list = [pv_23B18, pv_23B19, pv_23B20, pv_23B21, pv_23B22, pv_23B23, pv_23B24_H, pv_23B24_T, pv_CP_23B10, pv_CP_23B11, pv_CP_23B13, pv_CP_23B14_H, pv_CP_23B14_T, pv_CP_23B15, 			 pv_CP_23B16_H, pv_CP_23B16_T, pv_CP_23B17, pv_CP_23B25_H, pv_CP_23B25_T, pv_CP_23B26, pv_CP_23B27, pv_CP_23B28, pv_CP_23B29, pv_CP_23B30, pv_CP_23B31, 		 			 pv_CP_23M10_RET, pv_CP_23M7_RET, pv_CP_23M8_RET, pv_CP_23M9_FDB_Hz, pv_CP_23M9_Status, pv_CP_23X1_RET, pv_Emergencia_Gases, pv_StatusContatorAQ1, 			  			 pv_StatusContatorAQ1_1A, pv_StatusDisjuntorMotor1]

outputPVs_list = [pv_AQ_Reserve, pv_CP_PLUS_CP_23W3, pv_CP_23M10, pv_CP_23M12, pv_CP_23M7, pv_CP_23M8, pv_CP_23M9_ACK, pv_CP_23M9_Freq_Hz, pv_CP_23M9_Jog, pv_CP_23M9_On_Off, 			 pv_CP_23M9_On_Off, pv_CP_23M9_Reverso, pv_CP_23W2, pv_CP_23X1, pv_DQ_RESERVE1, pv_DQ_RESERVE2, pv_ResetSecuritySystem] 

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




