from src.archie import *
 


def dockerswarm_apply(workload):

    docker_swarm_enabled = workload.solutions.get("Docker_Swarm", BoolVal(False))

    if "Container runtime" in ROLES:
        track = f"Docker Swarm requires Docker when Container runtime is a role"
        constraint = Implies(docker_swarm_enabled, workload.solutions.get("Docker", BoolVal(False)))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Service mesh" in ROLES:
        track = f"Docker Swarm cannot be used with Istio when Service mesh is a role"
        constraint = Implies(docker_swarm_enabled, Not(workload.solutions.get("Istio", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

        track = f"Docker Swarm cannot be used with Linkerd when Service mesh is a role"
        constraint = Implies(docker_swarm_enabled, Not(workload.solutions.get("Linkerd", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


DockerSwarm = System(
    "Docker_Swarm",
    orchestrator,
    dockerswarm_apply,
)
