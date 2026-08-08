from src.archie import *
 


def istio_apply(workload):

    # Get all compute devices in the workload topology
    computes = workload.topology.get_children(device_type=DEVICE_TYPE.COMPUTE)
    istio_enabled = workload.solutions.get("Istio", BoolVal(False))

    if "Orchestrator" in ROLES:
        track = f"Istio excludes Docker Swarm when Orchestrator is a role"
        constraint = Implies(istio_enabled, Not(workload.solutions.get("Docker_Swarm", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if low_load in workload.properties or medium_load in workload.properties:
        track = f"Istio sidecar requires 2 GB memory per compute when load is low or medium, evidence through expert experience"
        constraint = Implies(istio_enabled, Implies(workload.solution_configs["Istio"]["sidecar"], And(*[c.constrained_slots["memory_GB"]["Istio"] <= 2 for c in computes])))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if not latency in workload.objectives or OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority:
        track = f"Istio requires sidecar when latency is not an objective or ease-of-deployment priority exceeds latency priority as ambient mode is hard to debug, troubleshoot, and there exists lesser documentation"
        constraint = Implies(istio_enabled, Not(workload.solution_configs["Istio"]["ambient"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if latency in workload.objectives:
        track = f"Istio excludes sidecar when latency is an objective due to performance overhead"
        constraint = Implies(istio_enabled, Not(workload.solution_configs["Istio"]["sidecar"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Os" in ROLES:
        track = f"Istio excludes Windows and Unix if Os is a role"
        constraint = Implies(istio_enabled, And(Not(workload.solutions.get("Windows", BoolVal(False))), Not(workload.solutions.get("Unix", BoolVal(False)))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if low_utilization in workload.objectives:
        track = f"Istio excludes sidecar when low utilization is an objective"
        constraint = Implies(istio_enabled, Not(workload.solution_configs["Istio"]["sidecar"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if not l7_load_balancing in workload.properties:
        track = f"Istio excludes ambient mode when L7 load balancing is not a workload property"
        constraint = Implies(istio_enabled, Not(workload.solution_configs["Istio"]["ambient"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


Istio = System(
    "Istio",
    service_mesh,
    istio_apply,
    configs=["sidecar", "ambient"]
)
