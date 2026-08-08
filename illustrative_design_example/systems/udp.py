from src.archie import *

def udp_apply(workload):
    if wan_flows in workload.properties or dc_flows in workload.properties and latency in workload.objectives:
        return True
    else:
        udp_False = Bool("udp_wan_flows_or_dc_flows_and_latency")
        VAR_DESCRIPTIONS["udp_False"] = "DC or WAN flows with latency objective for UDP"
        SOLVER.assert_and_track(udp_False == BoolVal(False), "track_udp_no_wan_flows_or_dc_flows_and_latency")
        TRACKED_CONSTRAINTS["track_udp_no_wan_flows_or_dc_flows_and_latency"] = (udp_False == False)
        return udp_False

UDP = System("UDP", transport, udp_apply)