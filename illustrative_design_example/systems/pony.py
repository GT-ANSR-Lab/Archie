from src.archie import *

def PONY_apply(workload):
    links = workload.topology.get_children(device_type = DEVICE_TYPE.LINK)
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["PONY"] == 2 for compute in computes])

PONY = System("PONY", transport, PONY_apply, objectives = [latency, throughput, ease_of_deployment])
