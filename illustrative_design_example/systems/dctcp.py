from src.archie import *

# Systems
def dctcp_apply(workload):
    if dc_flows in workload.properties and (short_flows in workload.properties or incast in workload.properties):
        routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
        return Implies(And(WORKLOAD_PROPERTIES[dc_flows.id], Or(WORKLOAD_PROPERTIES[short_flows.id], WORKLOAD_PROPERTIES[incast.id])),
                       And(*[router.configuration["ECN"] for router in routers]))
    else:
        dctcp_False = Bool("dctcp_dc_flows_and_short_or_incast")
        VAR_DESCRIPTIONS["dctcp_dc_flows_and_short_or_incast"] = "DC flows present for DCTCP with short flows or incast"
        SOLVER.assert_and_track(dctcp_False == BoolVal(False), "track_dctcp_no_dc_flows_and_short_or_incast")
        TRACKED_CONSTRAINTS["track_dctcp_no_dc_flows_and_short_or_incast"] = (dctcp_False == BoolVal(False))
        return dctcp_False


DCTCP = System("DCTCP", cca, dctcp_apply, objectives = [throughput, latency])