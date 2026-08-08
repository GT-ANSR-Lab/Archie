from src.archie import *

def srd_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    constraints = And(
        And(*[compute.configuration["SMART_NIC"] for compute in computes]),
    )
    return constraints

SRD = System("SRD", transport, srd_apply, objectives = [latency, throughput, ease_of_deployment])
