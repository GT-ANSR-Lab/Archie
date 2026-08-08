from src.archie import *

def bfc_apply(workload):
        routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
        links = workload.topology.get_children(device_type = DEVICE_TYPE.LINK)

        constraints = And(
            And(*[router.configuration["P4"] for router in routers]),
            And(*[router.constrained_slots["P4-stages"]["BFC"] == 8 for router in routers]),
            workload.solutions["RDMA"], WORKLOAD_PROPERTIES[dc_flows.id]
        )
        return And(constraints, 
                   Implies(Not(Or(WORKLOAD_PROPERTIES[short_flows.id], WORKLOAD_PROPERTIES[incast.id])),
                          And(*[link.configuration["bandwidth"] >= 100 for link in links])))

BFC = System("BFC", cca, bfc_apply, objectives = [throughput, latency])








