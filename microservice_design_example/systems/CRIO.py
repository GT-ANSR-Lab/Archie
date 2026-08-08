from src.archie import *
 


def crio_apply(workload):

    crio_enabled = workload.solutions.get("CRI-O", BoolVal(False))

    if "Orchestrator" in ROLES:
        track = f"CRI-O cannot be used with Docker Swarm when Orchestrator is a role"
        constraint = Implies(crio_enabled, Not(workload.solutions.get("Docker_Swarm", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if non_root in workload.properties:
        track = f"CRI-O is unavailable when user is non-root"
        constraint = Implies(crio_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint
        
    return BoolVal(True)


CRIO = System(
    "CRI-O",
    container_runtime,
    crio_apply,
)
