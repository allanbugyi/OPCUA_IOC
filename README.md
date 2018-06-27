EPICS IOC developed with SoftIoc framework from Diamond Light Source with support for OPC UA architecture, based on FreeOpcUa package. The IOC establishes a connection with an OPC UA server as a client, retrieving the nodes within the server's  address space. The IOC's PVs are created based on OPC UA XML schema provided as input to 'opcua_ioc' python script, i.e., all nodes contained in '<UAVariable>' tag are considered to be a potential PV, with the parent node serving as a filter to select which will be linked to an EPICS' record - when we say link, we mean that we create a record, of accordingly type, to receive updates from the mapped OPC UA node.

Functionalities
===============
- Automated PV generation in EPICS style format, from OPC UA XML schema;
- Read and write on PV's;
- Monitoring: periodically scan and datachange event.

Dependencies
============
For SoftIoc the dependencies are 'cothread' and 'epicsdbbuilder'. Both can be installed using 'setup.py' script. 
Observation: SoftIoc was run with python2.7 and apparently failed to compile with python 3.

In order to install FreeOpcUa, install the following python package 'opcua', with pip, as example. For details, check the github project in this link: (https://github.com/FreeOpcUa/python-opcua)

Running the IOC
===============
Run 'pythonIoc.in' followed by 'opcua_ioc' with the XML file as argument. 'IP:port' can also be provided as the third-argument and is optionall. For help, run 'opcua_ioc help'.

Development
===========
SoftIoc's documentation can be found in this link: (http://controls.diamond.ac.uk/downloads/python/pythonSoftIoc/2-11/html/index.html)

The IOC is currently on its first version 1.0 and its script 'opcua_ioc' is thoroughly commented.

For any other questions contact: (allan.bugyi@lnls.br)

Directory Structure
===================
bin/				Contains softIoc binary within a subdirectory named with the target architecture
dbd/				database definition files for softIoc
python/				softIoc python packages
opcua_ioc			IOC's python script
pythonIoc.in			IOC initialization file
HVAC.PLC_1.OPCUA.xml	 	OPC UA xml file for running tests
epicsdbbuilder-1.1/		SoftIoc dependency
cothread-2-14			SoftIoc dependency
pythonSoftIoc-2.11		SoftIoc source code


