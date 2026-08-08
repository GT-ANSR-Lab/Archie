from src.archie import *

def sonata_apply(workload):
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    return And(
        And(*[router.configuration["P4"] for router in routers]),
        And(*[router.constrained_slots["P4-stages"]["Sonata"] == 4 for router in routers]),
    )

SONATA = System("Sonata", monitor, sonata_apply)

# SuggestedOrdering("Sonata_mon", monitoring, SONATA, 20)