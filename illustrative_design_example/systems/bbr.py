from src.archie import *

def bbr_apply(workload):
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    # if high_priority in workload.objectives:
    #     return BoolVal(True)

    return Or(OBJECTIVES[high_priority.id], And(*[Sum([router.constrained_slots["QoS"][solution_id] for solution_id in SYSTEMS]) <= router.configuration["QoS"] - 1 for router in routers]))

BBR = System("BBR", cca, bbr_apply, objectives=[throughput, latency])