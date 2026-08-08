from src.archie import *

def r2p2_apply(workload):
    if dc_flows in workload.properties:
        routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
        return And(
            And(*[router.configuration["P4"] for router in routers]),
            And(*[router.constrained_slots["P4-stages"]["R2P2"] == 4 for router in routers]),
        )
    else:
        r2p2_False = Bool("r2p2_dc_flows")
        VAR_DESCRIPTIONS["r2p2_dc_flows"] = "DC flows present for R2P2"
        SOLVER.assert_and_track(r2p2_False == BoolVal(False), "track_r2p2_no_dc_flows")
        TRACKED_CONSTRAINTS["track_r2p2_no_dc_flows"] = (r2p2_False == False)
        return r2p2_False

R2P2 = System("R2P2", transport, r2p2_apply)

# SuggestedOrdering("R2P2_latency", latency, R2P2, 5)
# SuggestedOrdering("R2P2_throughput", throughput, R2P2, 5)
# SuggestedOrdering("R2P2_load_balancing", load_balancing, R2P2, 5)