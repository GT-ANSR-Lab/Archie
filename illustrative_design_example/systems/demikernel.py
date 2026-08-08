from src.archie import *

def demikernel_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(*[Not(workload_temp.solutions[system_id]) for compute in computes for workload_temp in compute.workloads for system_id in SYSTEMS if SYSTEMS[system_id].role == cpu_sched and not system_id == "Demikernel"])

DEMIKERNEL = System("Demikernel", cpu_sched, demikernel_apply, objectives = [latency, ease_of_deployment, application_modification, compute_efficiency, host_resource_isolation, throughput])