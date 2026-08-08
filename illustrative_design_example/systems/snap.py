from src.archie import *

def snap_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[Not(workload_temp.solutions[system_id]) for compute in computes for workload_temp in compute.workloads for system_id in SYSTEMS if SYSTEMS[system_id].role == cpu_sched and not system_id == "snap"]),
        Implies(workload.solution_configs["snap"]["PONY"], workload.solutions["PONY"])
    )

SNAP = System("snap", cpu_sched, snap_apply, objectives = [latency, compute_efficiency, ease_of_deployment, application_modification, host_resource_isolation, throughput], configs = ["PONY", "LINUX"])