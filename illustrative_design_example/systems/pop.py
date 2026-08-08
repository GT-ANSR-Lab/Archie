from src.archie import *

# Systems
def single_pop_apply(workload):
    dc = workload.topology.get_parents(devicegroup_type=DEVICEGROUP_TYPE.DC)
    POP_Router = Device(dc.id + "_POP", DEVICE_TYPE.ROUTER, hardware = ) # TODO: should we add single/distributed pop as a single hardware
    dc.set_property("POP", POP_Router)


def dist_pop_apply(workload):
    dc = workload.topology.get_parents(devicegroup_type=DEVICEGROUP_TYPE.DC)
    POP_Router = Device(dc.id + "_POP", DEVICE_TYPE.ROUTER, hardware = ) # TODO: should we add single/distributed pop as a single hardware
    dc.set_property("POP", POP_Router)


SINGLE_POP = System("Single_Pop", INTERNET, single_pop_apply)
DIST_POP = System("Dist_Pop", INTERNET, dist_pop_apply)

# SuggestedOrdering("Single_Pop_Firewall", fault_tolerance, SINGLE_POP, 0)
# SuggestedOrdering("Dist_Pop_Firewall", fault_tolerance, DIST_POP, 3)

