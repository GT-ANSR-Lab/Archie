from src.archie import *

def shenango_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[compute.constrained_slots["cores"]["Shenango"] == 1 for compute in computes]),
        And(*[Not(workload_temp.solutions[system_id]) for compute in computes for workload_temp in compute.workloads for system_id in SYSTEMS if SYSTEMS[system_id].role == cpu_sched and not system_id == "Shenango"]),
    )

SHENANGO = System("Shenango", cpu_sched, shenango_apply, objectives = [latency, compute_efficiency, ease_of_deployment, application_modification, host_resource_isolation, throughput])