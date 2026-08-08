from src.archie import *

def conga_apply(workload):
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    return And(*[router.constrained_slots["memory"]["Conga"] == 0.2*workload.network_load for router in routers])

CONGA = System("Conga", load_balancer, conga_apply, objectives = [load_balancing])