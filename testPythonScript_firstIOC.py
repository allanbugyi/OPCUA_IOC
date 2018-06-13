# DLS requires
from pkg_resources import require
require('cothread==2.14')
require('epicsdbbuilder==development')

# Import basic softioc framework
from softioc import softioc, builder, device

#FreeOpcUa python package
from opcua import Client, ua

# Create PVs
builder.SetDeviceName('CP_HVAC')
pv_Temperatura_CP_1 = builder.boolIn("Temperatura_CP_1", ZNAM=False, ONAM=True)
pv_23B18 = builder.longIn("23B18", SCAN="1 second")
#pv_Temperatura_CP_1.set("False")
client = Client("opc.tcp://10.2.121.202:4840")

try:
     client.connect()
     root = client.get_root_node()
     print("Objects node is: ", root)
     children = root.get_children()
     print(children)
     #child = root.get_child(["Temperatura_CP_2"])
     #print(child)
     #var = client.get_node("ns=3; s=&quot")
     #var = client.get_node(".&quot;Temperatura_CP_1&quot")
     #var = client.get_node("3:Temperatura_CP_1")
     var = client.get_node(ua.NodeId(85))
     print(var)
     print(var.get_browse_name())       
     children2 = var.get_children()
     print(children2)
     childOfVar = client.get_node("ns=3;s=PLC")
     childOfChildOfVar = client.get_node("ns=3;s=Inputs")
     pv = childOfChildOfVar.get_child("3:Emergencia_Gases")
     pv2 = childOfChildOfVar.get_child("3:23B18")
     print(pv2.get_value())
     pv_23B18.set(int (pv2.get_value()))
#     pv_Temperatura_CP_1.set(bool (pv.get_value()))
     #pv_Temperatura_CP_1.trigger()
    # print(pv_Temperatura_CP_1.get())
     print(pv_23B18.get())
finally:
    client.disconnect()


# Run the IOC.  This is boilerplate, and must always be done in this order,
# and must always be done after creating all PVs.
builder.LoadDatabase()
softioc.iocInit()

softioc.interactive_ioc(globals())
