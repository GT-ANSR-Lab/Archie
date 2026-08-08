from src.archie import *

def ledbat_apply(workload):
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    return And(*[router.constrained_slots["memory"]["LEDBAT"] >= 10 for router in routers])

LEDBAT = System("LEDBAT", cca, ledbat_apply, objectives = [scavenger])

# SuggestedOrdering("LEDBAT_scavenger", scavenger, LEDBAT, 10)

# LEDBAT.add_warning(lambda workload: has_small_buffers(workload.topology), "LEDBAT needs deep buffers...")
