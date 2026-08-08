from src.archie import *
 

def keda_apply(workload):
    keda_enabled = workload.solutions.get("KEDA", BoolVal(False))

    if "Orchestrator" in ROLES:
        track = f"KEDA requires Kubernetes orchestrator or Knative when Orchestrator is a role"
        constraint = Implies(keda_enabled, Or(workload.solutions.get("Kubernetes_orchestrator", BoolVal(False)), workload.solutions.get("Knative", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and (low_load in workload.properties or medium_load in workload.properties) and heterogenous in workload.properties:
        track = f"KEDA is not recommended when ease of deployment is an objective with low-or-medium heterogeneous load as it requires configuration of metric policies that are not required with such loads i.e memory and CPU usage are sufficient metrics"
        constraint = Implies(keda_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and tls in workload.properties:
        track = f"KEDA is unavailable when ease of deployment is an objective and TLS is a property due to more number of steps to configure KEDA with TLS"
        constraint = Implies(keda_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


KEDA = System(
    "KEDA",
    autoscaler,
    keda_apply,
)
