from src.archie import *
 


def docker_apply(workload):

    docker_enabled = workload.solutions.get("Docker", BoolVal(False))

    if ease_of_deployment in workload.objectives and "Orchestrator" in ROLES:
        track = f"Docker cannot be used with Kubernetes orchestrator when ease of deployment is an objective and Orchestrator is a role"
        constraint = Implies(docker_enabled, Not(And(workload.solutions.get("Kubernetes_orchestrator", BoolVal(False)), workload.solutions.get("Knative", BoolVal(False)))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Orchestrator" in ROLES:
        track = f"Docker requires the in-cluster configuration when Docker Swarm is enabled and Orchestrator is a role"
        constraint = Implies(docker_enabled, Implies(workload.solutions.get("Docker_Swarm", BoolVal(False)), workload.solution_configs["Docker"]["in-cluster"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if latency or ease_of_deployment and "Os" in ROLES:
        track = f"Docker cannot be used on Windows and Unix when latency is an objective or ease of deployment is an objective with Os as a role"
        constraint = Implies(docker_enabled, And(Not(workload.solutions.get("Windows", BoolVal(False))), Not(workload.solutions.get("Unix", BoolVal(False)))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if non_root in workload.properties:
        track = f"Docker is unavailable when user is non-root"
        constraint = Implies(docker_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


Docker = System(
    "Docker",
    container_runtime,
    docker_apply,
    configs=["stand-alone", "in-cluster"]
)
