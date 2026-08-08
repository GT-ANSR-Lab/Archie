from src.archie import *
 


def linkerd_apply(workload):

    linkerd_enabled = workload.solutions.get("Linkerd", BoolVal(False))

    if "Orchestrator" in ROLES:
        track = f"Linkerd excludes Docker Swarm when Orchestrator is a role"
        constraint = Implies(linkerd_enabled, Not(workload.solutions.get("Docker_Swarm", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Os" in ROLES:
        track = f"Linkerd requires Linux when ease of deployment is an objective and Os is a role"
        constraint = Implies(linkerd_enabled, workload.solutions.get("Linux", BoolVal(False)))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and "Autoscaler" in ROLES:
        track = f"Linkerd excludes KEDA when ease of deployment is an objective and Autoscaler is a role"
        constraint = Implies(linkerd_enabled, Not(workload.solutions.get("KEDA", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint
    
    if latency in workload.objectives and high_load in workload.properties:
        track = f"Linkerd is unavailable when latency is an objective and the workload has High Load"
        constraint = Implies(linkerd_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


Linkerd = System(
    "Linkerd",
    service_mesh,
    linkerd_apply
)
