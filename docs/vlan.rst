##########################
Virtual Local Area Network
##########################

The TestFramework depends heavily on the possibilities of VLANs.
Each router has its own VLAN with its VLAN ID to separate it from others routers.
For this functionality you need a network switch with VLAN capabilities.

Important python packages:
    - pyroute2
    - paramiko

(the documentation is here not complete because the auto including function is corrupted by the pyroute2 module)


Class NetworkCtrl
=================
.. automodule:: network.network_ctrl
  :members:

Class Namespace
===============
.. automodule:: network.namespace
  :members:

Class NVAssistent
=================
.. automodule:: network.nv_assist
  :members:



