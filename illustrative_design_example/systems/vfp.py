from src.archie import *

def vfp_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[compute.configuration["FPGA"] for compute in computes]),
        And(*[compute.constrained_slots["FPGA-capacity"]["VFP"] == 10 for compute in computes]),
    )

VFP = System("VFP", virtual_switch, vfp_apply, objectives = [ease_of_deployment])

# SuggestedOrdering("VFP_multiten", multi_tenancy, VFP, 1)
# SuggestedOrdering("VFP_sec", security, VFP, 1)
# SuggestedOrdering("VFP_isol", host_resource_isolation, VFP, 1)


# 3 types of NIC - (Smart/fixed-function - FPGA, CPU, P4), (RDMA/Non-RDMA)
# Ease of deployment - CPU > FPGA > P4 (Line rate is the reverse order, Programabbility is the same)
