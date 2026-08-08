from src.archie import *

PINGMESH_CPU_FACTOR = 0.2

def pingmesh_apply(workload):
    computes = workload.topology.get_children(DEVICE_TYPE.COMPUTE)
    return And(*[compute.constrained_slots["cores"]["PingMesh"] == PINGMESH_CPU_FACTOR * len(computes) for compute in computes])

PINGMESH = System("PINGMESH", monitor, pingmesh_apply)

# SuggestedOrdering("PingMesh_mon", monitoring, PINGMESH, 1)