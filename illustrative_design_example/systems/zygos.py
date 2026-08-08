from src.archie import *

def ZygOS_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[Not(workload_temp.solutions[system_id]) for compute in computes for workload_temp in compute.workloads for system_id in SYSTEMS if SYSTEMS[system_id].role == cpu_sched and not system_id == "ZygOS"]),
        And(*[compute.constrained_slots["cores"]["ZygOS"] == 1 for compute in computes])
    )

ZYGOS = System("ZygOS", cpu_sched, ZygOS_apply, objectives = [latency, compute_efficiency, ease_of_deployment, application_modification, host_resource_isolation, throughput])