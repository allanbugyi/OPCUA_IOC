# -*- coding: utf8 -*-
from pkg_resources import require
require('cothread==2.14')
require('epicsdbbuilder==development')

# Import basic Diamond softioc framework
from softioc import softioc, builder, device

#FreeOpcUa python package
from opcua import Client, ua

#Set IOC's name
builder.SetDeviceName('CP_HVAC')

#Create PVs
#PLC INPUT PVs
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

#PLC OUTPUT PVs
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

#Create OPCUA client
client = Client("opc.tcp://10.2.121.202:4840")

try:
	#Establish connection with OPC UA Server
	client.connect()

	#OPC UA parent Node from INPUT PVs
	parentNode_INPUT_PVs = client.get_node("ns=3;s=Inputs")
     
	#OPC UA parent Node from OUTPUT PVs
	parentNode_OUTPUT_PVs = client.get_node("ns=3;s=Outputs")

	#Read routine for the PVs
	pv_23B18_aux            = parentNode_INPUT_PVs.get_child("3:23B18")
	pv_23B18.set(int (pv_23B18_aux.get_value()))
	pv_23B19_aux            = parentNode_INPUT_PVs.get_child("3:23B19")
	pv_23B19.set(pv_23B19_aux.get_value())
	pv_23B20_aux            = parentNode_INPUT_PVs.get_child("3:23B20")
	pv_23B20.set(pv_23B20_aux.get_value())
	pv_23B21_aux            = parentNode_INPUT_PVs.get_child("3:23B21")
	pv_23B21.set(pv_23B21_aux.get_value())
	pv_23B22_aux            = parentNode_INPUT_PVs.get_child("3:23B22")
	pv_23B22.set(pv_23B22_aux.get_value())
	pv_23B23_aux            = parentNode_INPUT_PVs.get_child("3:23B23")
	pv_23B23.set(pv_23B23_aux.get_value())
	pv_23B24_H_aux          = parentNode_INPUT_PVs.get_child("3:23B24_H")
	pv_23B24_H.set(pv_23B24_H_aux.get_value())
	pv_23B24_T_aux          = parentNode_INPUT_PVs.get_child("3:23B24_T")
	pv_23B24_T.set(pv_23B24_T_aux.get_value())
	pv_CP_23B10_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B10")
	pv_CP_23B10.set(pv_CP_23B10_aux.get_value())
	pv_CP_23B11_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B11")
	pv_CP_23B11.set(pv_CP_23B11_aux.get_value())
	pv_CP_23B13_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B13")
	pv_CP_23B13.set(pv_CP_23B13_aux.get_value())
	pv_CP_23B14_H_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B14_H")
	pv_CP_23B14_H.set(pv_CP_23B14_H_aux.get_value())
	pv_CP_23B14_T_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B14_T")
	pv_CP_23B14_T.set(pv_CP_23B14_T_aux.get_value())
	pv_CP_23B15_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B15")
	pv_CP_23B15.set(pv_CP_23B15_aux.get_value())
	pv_CP_23B16_H_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B16_H")
	pv_CP_23B16_H.set(pv_CP_23B16_H_aux.get_value())
	pv_CP_23B16_T_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B16_T")
	pv_CP_23B16_T.set(pv_CP_23B16_T_aux.get_value())
	pv_CP_23B17_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B17")
	pv_CP_23B17.set(pv_CP_23B17_aux.get_value())
	pv_CP_23B25_H_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B25_H")
	pv_CP_23B25_H.set(pv_CP_23B25_H_aux.get_value())
	pv_CP_23B25_T_aux       = parentNode_INPUT_PVs.get_child("3:CP-23B25_T")
	pv_CP_23B25_T.set(pv_CP_23B25_T_aux.get_value())
	pv_CP_23B26_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B26")
	pv_CP_23B26.set(pv_CP_23B26_aux.get_value())
	pv_CP_23B27_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B27")
	pv_CP_23B27.set(pv_CP_23B27_aux.get_value())
	pv_CP_23B28_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B28")
	pv_CP_23B28.set(pv_CP_23B28_aux.get_value())
	pv_CP_23B29_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B29")
	pv_CP_23B29.set(pv_CP_23B29_aux.get_value())
	pv_CP_23B30_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B30")
	pv_CP_23B30.set(pv_CP_23B30_aux.get_value())
	pv_CP_23B31_aux         = parentNode_INPUT_PVs.get_child("3:CP-23B31")
	pv_CP_23B31.set(pv_CP_23B31_aux.get_value)
	pv_CP_23M10_RET_aux     = parentNode_INPUT_PVs.get_child("3:CP-23M10_RET")
	pv_CP_23M10_RET.set(pv_CP_23M10_RET_aux.get_value())
	pv_CP_23M7_RET_aux      = parentNode_INPUT_PVs.get_child("3:CP-23M7_RET")
	pv_CP_23M7_RET.set(pv_CP_23M7_RET_aux.get_value())
	pv_CP_23M8_RET_aux      = parentNode_INPUT_PVs.get_child("3:CP-23M8_RET")
	pv_CP_23M8_RET.set(pv_CP_23M8_RET_aux.get_value())
	pv_CP_23M9_FDB_Hz_aux   = parentNode_INPUT_PVs.get_child("3:CP-23M9_FDB_Hz")
	pv_CP_23M9_FDB_Hz.set(pv_CP_23M9_FDB_Hz_aux.get_value())
	pv_CP_23M9_Status_aux   = parentNode_INPUT_PVs.get_child("3:CP-23M9_Status")
	pv_CP_23M9_Status.set(pv_CP_23M9_Status_aux.get_value())
	pv_CP_23X1_RET_aux      = parentNode_INPUT_PVs.get_child("3:CP-23X1_RET")
	pv_CP_23X1_RET.set(pv_CP_23X1_RET_aux.get_value())
	pv_Emergencia_Gases_aux = parentNode_INPUT_PVs.get_child("3:Emergencia_Gases")
	pv_Emergencia_Gases.set(pv_Emergencia_Gases_aux.get_value())
	pv_StatusContatorAQ1_aux= parentNode_INPUT_PVs.get_child("3:Status Contator AQ1") 
	pv_StatusContatorAQ1.set(pv_StatusContatorAQ1_aux.get_value())
	pv_StatusContatorAQ1_1A_aux = parentNode_INPUT_PVs.get_child("3:Status Contator AQ1.1A")
	pv_StatusContatorAQ1_1A.set(pv_StatusContatorAQ1_1A_aux.get_value())
	pv_StatusDisjuntorMotor1_aux = parentNode_INPUT_PVs.get_child("3:Status Disjuntor Motor 1") 
	pv_StatusDisjuntorMotor1.set(pv_StatusDisjuntorMotor1_aux.get_value())

	#pv_Emergencia_Gases = parentNode_PVs.get_child("3:Emergencia_Gases")
     	#pv_Temperatura_CP_1.set(bool (pv.get_value()))

finally:
    client.disconnect()

# Run the IOC.  This is boilerplate, and must always be done in this order,
# and must always be done after creating all PVs.
builder.LoadDatabase()
softioc.iocInit()
pv_23B18.set(10)
softioc.interactive_ioc(globals())

