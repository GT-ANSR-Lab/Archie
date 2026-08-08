from src.archie import *


def create_topology():
    '''
    |-----------|      |-----------|
    |           |      |           |     
    |   RACK1   |      |   RACK2   | 
    |  5 nodes  |      |  5 nodes  |
    |-----------|      |-----------|
    '''

    rack0 = DeviceGroup("rack0", DEVICEGROUP_TYPE.RACK)
    rack0.add_children([Device("node0", DEVICE_TYPE.COMPUTE), Device("node1", DEVICE_TYPE.COMPUTE), Device("node2", DEVICE_TYPE.COMPUTE), Device("node3", DEVICE_TYPE.COMPUTE), Device("node4", DEVICE_TYPE.COMPUTE)])
    rack1 = DeviceGroup("rack1", DEVICEGROUP_TYPE.RACK)
    rack1.add_children([Device("node5", DEVICE_TYPE.COMPUTE), Device("node6", DEVICE_TYPE.COMPUTE), Device("node7", DEVICE_TYPE.COMPUTE), Device("node8", DEVICE_TYPE.COMPUTE), Device("node9", DEVICE_TYPE.COMPUTE)])
    pod = DeviceGroup("pod1", DEVICEGROUP_TYPE.POD)
    pod.add_children([rack0, rack1])
    return pod