from src.archie import *

def andromeda_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[compute.constrained_slots["cores"]["ANDROMEDA"] == 1 for compute in computes]),
    )

ANDROMEDA = System("ANDROMEDA", virtual_switch, andromeda_apply, objectives = [ease_of_deployment])


