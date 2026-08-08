from src.archie import *

def annulus_apply(workload):
    tor_router = workload.topology.devicegroup_properties["TOR"]
    return And(
        tor_router.configuration["ECN"]
    )

ANNULUS = System("Annulus", WAN_DC_COMPETITION, annulus_apply)

# SuggestedOrdering("Annulus_th", throughput, ANNULUS, 5)
# SuggestedOrdering("Annulus_lat", latency, ANNULUS, 5)