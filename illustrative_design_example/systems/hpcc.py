from src.archie import *

def hpcc_apply(workload):
    if dc_flows in workload.properties and (short_flows in workload.properties or incast in workload.properties) and latency in workload.objectives and throughput in workload.objectives:
        routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
        return (Implies(And(
                        WORKLOAD_PROPERTIES[dc_flows.id], 
                        Or(WORKLOAD_PROPERTIES[short_flows.id], WORKLOAD_PROPERTIES[incast.id]), 
                        OBJECTIVES[latency.id], 
                        OBJECTIVES[throughput.id]), 
                        And(*[router.configuration["INT"] for router in routers])))
    else:
        hpcc_False = Bool("hpcc_dc_flows_and_short_flows_or_incast_and_latency_or_throughput")
        VAR_DESCRIPTIONS["hpcc_dc_flows_and_short_flows_or_incast_and_latency_or_throughput"] = "HPCC dc flows and (short flows or incast) and (latency or throughput) objectives"
        SOLVER.assert_and_track(hpcc_False == BoolVal(False), "track_hpcc_no_dc_flows_and_short_flows_or_incast_and_latency_or_throughput")
        TRACKED_CONSTRAINTS["track_hpcc_no_dc_flows_and_short_flows_or_incast_and_latency_or_throughput"] = (hpcc_False == False)
        return hpcc_False

HPCC = System("HPCC", cca, hpcc_apply)