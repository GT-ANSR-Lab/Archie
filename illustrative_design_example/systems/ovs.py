from src.archie import *

def ovs_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["OVS"] == 2 for compute in computes])

OVS = System("OVS", virtual_switch, ovs_apply)

# SuggestedOrdering("OVS_multiten", multi_tenancy, OVS, 5)
# SuggestedOrdering("OVS_sec", security, OVS, 5)
# SuggestedOrdering("OVS_isol", isolation, OVS, 5)
