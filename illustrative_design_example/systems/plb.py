from src.archie import *

def plb_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["PLB"] == 0.25 for compute in computes])

PLB = System("PLB", load_balancer, plb_apply, objectives = [load_balancing])