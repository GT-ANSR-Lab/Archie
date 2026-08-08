from src.archie import *

def tonic_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[compute.configuration["FPGA"] for compute in computes])
    )

TONIC = System("Tonic", transport, tonic_apply)

# SuggestedOrdering("Tonic_latency", latency, TONIC, 1)