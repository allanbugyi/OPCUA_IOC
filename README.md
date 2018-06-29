EPICS IOC developed with SoftIoc framework from Diamond Light Source with support for OPC UA architecture, based on FreeOpcUa package. The IOC establishes a connection with an OPC UA server as a client, retrieving the nodes within the server's  address space. The IOC's PVs are created based on OPC UA XML schema provided as input to 'opcua_ioc' python script, i.e., all nodes contained in 'UAVariable' tag are considered to be a potential PV, with the parent node serving as a filter to select which will be linked to an EPICS' record - when we say link, we mean that we create a record, of accordingly type, to receive updates from the mapped OPC UA node.

Functionalities
===============
- Automated PV generation in EPICS style format, from OPC UA XML schema;
- Read and write on PV's;
- Monitoring: periodically scan and datachange event.

Dependencies
============
Python version: 3
Tested with Python 3.5.3

For SoftIoc the dependencies are 'cothread' (run 'pip3 install cothread') and 'epicsdbbuilder'(inside its subdirectory run 'python3 setup.py install'). 

In order to install 'FreeOpcUa', run 'pip3 install opcua'. For details, check the github project in this link: (https://github.com/FreeOpcUa/python-opcua)

Running the IOC
===============
Run './pythonIoc opcua_ioc' with the XML file as the first argument. 'IP:port' can also be provided as the third-argument and is optionall. For help, run './pythonIoc opcua_ioc help'.

Development
===========
SoftIoc's documentation can be found in this link: (http://controls.diamond.ac.uk/downloads/python/pythonSoftIoc/2-11/html/index.html)
For more details, check its github project: (https://github.com/Araneidae/pythonIoc)

The IOC is currently on its first version 1.0 and its script is thoroughly commented.

For any other questions contact: (allan.bugyi@lnls.br)

Directory Structure
===================
bin/				Contains softIoc binary within a subdirectory named with the target architecture
dbd/				Database definition files for softIoc
python/				SoftIoc python packages
opcua_ioc			* IOC's python script * 
pythonIoc			IOC initialization file
HVAC.PLC_1.OPCUA.xml	 	OPC UA xml file for running tests
epicsdbbuilder			SoftIoc dependency
pythonIoc_src			SoftIoc source code


