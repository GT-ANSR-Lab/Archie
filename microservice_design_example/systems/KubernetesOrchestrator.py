from src.archie import *
 


def kubernetes_orchestrator_apply(workload):

    computes = workload.topology.get_children(device_type=DEVICE_TYPE.COMPUTE)
    kubernetes_orchestrator_enabled = workload.solutions.get("Kubernetes_orchestrator", BoolVal(False))

    if ease_of_deployment in workload.objectives and "Container runtime" in ROLES:
        track = f"Kubernetes orchestrator excludes Docker when ease of deployment is an objective and Container runtime is a role"
        constraint = Implies(kubernetes_orchestrator_enabled, Not(workload.solutions.get("Docker", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Os" in ROLES:
        track = f"Kubernetes orchestrator requires Linux when Os is a role"
        constraint = Implies(kubernetes_orchestrator_enabled, workload.solutions.get("Linux", BoolVal(False)))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if latency in workload.objectives and ease_of_deployment not in workload.objectives:
        track = f"Kubernetes orchestrator is configured with eBPF when latency is an objective without ease of deployment"
        constraint = Implies(kubernetes_orchestrator_enabled, workload.solution_configs["Kubernetes_orchestrator"]["eBPF"])
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and fixed_arch in workload.properties:
        track = f"Kubernetes orchestrator requires matching compute architectures when ease of deployment is an objective and Fixed-arch is a property as multi-image registries are required otherwise"
        constraint = Implies(kubernetes_orchestrator_enabled, And(*[computes[0].configurations.get("arch", "") == c.configurations.get("arch", "") for c in computes]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint


    return BoolVal(True)


Kubernetes_orchestrator = System(
    "Kubernetes_orchestrator",
    orchestrator,
    kubernetes_orchestrator_apply,
    configs=["eBPF", "non-eBPF"]
)
