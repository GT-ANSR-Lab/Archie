from src.archie import *

def packetspray_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.configuration["NIC_Reorder_Buffer"] > 20 for compute in computes])

PACKETSPRAY = System("PacketSpray", load_balancer, packetspray_apply, objectives = [load_balancing])