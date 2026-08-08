from src.archie import *

def terminating_proxy_apply(workload):
    if wan_flows in workload.properties and latency in workload.objectives:
        return workload.topology.devicegroup_properties["TOP_SWITCH"].constrained_slots["cores"]["TerminatingProxy"] == 20
    else:
        return False

TERMINATING_PROXY = System("TerminatingProxy", WAN_DC_COMPETITION, terminating_proxy_apply)

# SuggestedOrdering("TerminatingProxy_th", throughput, TERMINATING_PROXY, 5)
# SuggestedOrdering("TerminatingProxy_lat", latency, TERMINATING_PROXY, 5)
# SuggestedOrdering("TerminatingProxy_firewall", security, TERMINATING_PROXY, 5)
# SuggestedOrdering("TerminatingProxy_monitoring", monitoring, TERMINATING_PROXY, 5)