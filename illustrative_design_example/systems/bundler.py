from src.archie import *

def bundler_apply(workload):
    if wan_flows in workload.properties and latency in workload.objectives:
        tor_router = workload.topology.devicegroup_properties["TOR"]
        return And(
            tor_router.configuration["ECN"]
        )
    else:
        bundler_False = Bool("bundler_wan_flows_and_latency")
        VAR_DESCRIPTIONS["bundler_wan_flows_and_latency"] = "WAN flows present for Bundler with Latency objective"
        SOLVER.assert_and_track(bundler_False == BoolVal(False), "track_bundler_no_wan_flows_and_latency")
        TRACKED_CONSTRAINTS["track_bundler_no_wan_flows_and_latency"] = (bundler_False == BoolVal(False))
        return bundler_False

BUNDLER = System("Bundler", ENHANCER, bundler_apply)