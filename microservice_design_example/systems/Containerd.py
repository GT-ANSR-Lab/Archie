from src.archie import *
 

def containerd_apply(workload):

    containerd_enabled = workload.solutions.get("Containerd", BoolVal(False))

    if monitoring in workload.objectives and latency in workload.objectives and not ease_of_deployment in workload.objectives:
        track = f"{workload.id}: Containerd requires the eBPF config when monitoring and latency are objectives without ease of deployment"
        constraint = Implies(containerd_enabled, workload.solution_configs["Containerd"]["eBPF"])
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if non_root in workload.properties:
        track = f"{workload.id}: Containerd is unavailable when user is non-root"
        constraint = Implies(containerd_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and "Os" in ROLES:
        track = f"{workload.id}: Containerd does not work on Unix and Windows when ease of deployment is an objective and OS is a role"
        constraint = Implies(containerd_enabled, And(Not(workload.solutions.get("Unix", BoolVal(False))), Not(workload.solutions.get("Windows", BoolVal(False)))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint
    
    track = f"{workload.id}: Containerd requires the in-cluster configuration"
    constraint = Implies(containerd_enabled, workload.solution_configs["Containerd"]["in-cluster"])
    SOLVER.assert_and_track(constraint, track)
    TRACKED_CONSTRAINTS[track] = constraint

    if "Orchestrator" in ROLES:
        track = f"{workload.id}: Containerd cannot be used with Docker Swarm when Orchestrator is a role"
        constraint = Implies(containerd_enabled, Not(workload.solutions.get("Docker_Swarm", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ui in workload.properties and ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority:
        track = f"{workload.id}: Containerd is unavailable when the workload has a UI property and ease of deployment is an objective"
        constraint = Implies(containerd_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


Containerd = System(
    "Containerd",
    container_runtime,
    containerd_apply,
    configs=["stand-alone", "in-cluster"]
)
