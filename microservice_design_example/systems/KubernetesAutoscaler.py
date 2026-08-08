from src.archie import *
 


def kubernetes_autoscaler_apply(workload):

    kubernetes_autoscaler_enabled = workload.solutions.get("Kubernetes_autoscaler", BoolVal(False))

    if "Orchestrator" in ROLES:
        track = f"Kubernetes autoscaler requires Kubernetes orchestrator or Knative when Orchestrator is a role"
        constraint = Implies(kubernetes_autoscaler_enabled, Or(workload.solutions.get("Kubernetes_orchestrator", BoolVal(False)), workload.solutions.get("Knative", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and "Orchestrator" in ROLES:
        track = f"Kubernetes autoscaler excludes Knative when ease of deployment is an objective and Orchestrator is a role due to additional configuration steps"
        constraint = Implies(kubernetes_autoscaler_enabled, Not(workload.solutions.get("Knative", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and "Service mesh" in ROLES:
        track = f"Kubernetes autoscaler excludes Istio when ease of deployment is an objective and Service mesh is a role because of additional configuration steps"
        constraint = Implies(kubernetes_autoscaler_enabled, Not(workload.solutions.get("Istio", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and tls in workload.properties:
        track = f"Kubernetes autoscaler is unavailable when ease of deployment is an objective and TLS is a property due to additional documentation consumption"
        constraint = Implies(kubernetes_autoscaler_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if cost_efficiency in workload.objectives and low_load in workload.properties:
        track = f"Kubernetes autoscaler is unavailable when COST is an objective and the workload has Low Load due to unnecessary resource usage because it can't scale to zero"
        constraint = Implies(kubernetes_autoscaler_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)

Kubernetes_autoscaler = System(
    "Kubernetes_autoscaler",
    autoscaler,
    kubernetes_autoscaler_apply,
)
