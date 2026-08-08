from src.archie import *

def homa_apply(workload):
    if dc_flows in workload.properties:
        routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
        return Implies(WORKLOAD_PROPERTIES[dc_flows.id], And(*[router.constrained_slots["QoS"][solution_id] == 0 for router in routers for solution_id in router.constrained_slots["QoS"]]))
    else:
        homa_False = Bool("homa_dc_flows")
        VAR_DESCRIPTIONS["homa_dc_flows"] = "DC flows present for Homa"
        SOLVER.assert_and_track(homa_False == BoolVal(False), "track_homa_no_dc_flows")
        TRACKED_CONSTRAINTS["track_homa_no_dc_flows"] = (homa_False == False)
        return homa_False


HOMA = System("HOMA", transport, homa_apply)