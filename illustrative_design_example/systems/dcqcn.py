from src.archie import *

# Systems
def dcqcn_apply(workload):
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    # if high_priority in workload.objectives:
    #     return workload.solutions["RDMA"]

    return And((Implies(OBJECTIVES[high_priority.id], workload.solutions["RDMA"])),
        And(*[Sum([router.constrained_slots["QoS"][solution_id] for solution_id in SYSTEMS]) <= router.configuration["QoS"] - 1 for router in routers]),
    )

DCQCN = System("DCQCN", cca, dcqcn_apply, objectives = [throughput, latency])

# SuggestedOrdering("DCQCN_th", throughput, DCQCN, 1)
# SuggestedOrdering("DCQCN_lat", latency, DCQCN, 1)