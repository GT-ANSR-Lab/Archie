from src.archie import *

def timely_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    constraints = And(WORKLOAD_PROPERTIES[dc_flows.id], Or(WORKLOAD_PROPERTIES[short_flows.id], WORKLOAD_PROPERTIES[incast.id]))

    # if high_priority in workload.objectives:
    #     return And(constraints, *[compute.configuration["NIC_TIMESTAMPS"] for compute in computes])
    constraints = And(constraints, 
                      Implies(OBJECTIVES[high_priority.id], And(*[compute.configuration["NIC_TIMESTAMPS"] for compute in computes])))

    return And(constraints, Implies(Not(OBJECTIVES[high_priority.id]),
        And(*[compute.configuration["NIC_TIMESTAMPS"] for compute in computes]),
        And(*[router.constrained_slots["QoS"]["Timely"] == 1 for router in routers])
        ))

TIMELY = System("Timely", cca, timely_apply, objectives = [throughput, latency])
