from src.archie import *

def eqds_linux_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["eqds_linux"] == 0.02 * workload.pps for compute in computes])

def eqds_dpdk_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["eqds_dpdk"] == 2 for compute in computes])



EQDS_DPDK = System("eqds_dpdk", ENHANCER, eqds_dpdk_apply)
EQDS_LINUX = System("eqds_linux", ENHANCER, eqds_linux_apply)

# SuggestedOrdering("eqds_linux_jitter", jitter, EQDS_LINUX, 3)
# SuggestedOrdering("eqds_dpdk_jitter", jitter, EQDS_DPDK, 4)

# SuggestedOrdering("eqds_linux_fct", fct, EQDS_LINUX, 2)
# SuggestedOrdering("eqds_dpdk_fct", fct, EQDS_DPDK, 2)

