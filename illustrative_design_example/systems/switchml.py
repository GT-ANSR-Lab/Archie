from src.archie import *

def switchML_apply(workload):
    if ml_training not in workload.properties:
        return False
    routers = workload.topology.get_children(device_type = DEVICE_TYPE.ROUTER)
    return And(
        And(*[router.configuration["P4"] for router in routers]),
        And(*[router.constrained_slots["P4-stages"]["SwitchML"] == 12 for router in routers]),
    )

SWITCHML = System("SwitchML", ENHANCER, switchML_apply)

# SuggestedOrdering("SWITCHML_throughput", throughput, SWITCHML, 50)