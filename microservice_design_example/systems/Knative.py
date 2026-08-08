from src.archie import *
 


def knative_apply(workload):

    knative_enabled = workload.solutions.get("Knative", BoolVal(False))

    if ease_of_deployment in workload.objectives and "Container runtime" in ROLES:
        track = f"Knative orchestrator excludes Docker when ease of deployment is an objective and Container runtime is a role"
        constraint = Implies(knative_enabled, Not(workload.solutions.get("Docker", BoolVal(False))))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if "Os" in ROLES:
        track = f"Knative orchestrator requires Linux when Os is a role"
        constraint = Implies(knative_enabled, workload.solutions.get("Linux", BoolVal(False)))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and fixed_arch in workload.properties:
        track = f"Knative orchestrator requires matching compute architectures when ease of deployment is an objective and Fixed-arch is a property"
        constraint = Implies(knative_enabled, And(*[computes[0].configurations.get("arch", "") == c.configurations.get("arch", "") for c in computes]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and (low_load in workload.properties or medium_load in workload.properties) and heterogenous in workload.properties:
        track = f"Knative is not recommended when ease of deployment is an objective with low-or-medium heterogeneous load as it requires configuration of metric policies that are not required with such loads i.e memory and CPU usage are sufficient metrics"
        constraint = Implies(knative_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    if ease_of_deployment in workload.objectives and not cost_efficiency in workload.properties:
        track = f"Knative is not recommended when ease of deployment is an objective with cost not as a property as scale-down-to-zero brings additional config and fine-tuning complexities"
        constraint = Implies(knative_enabled, BoolVal(False))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint


    return BoolVal(True)


Knative = System(
    "Knative",
    orchestrator,
    knative_apply,
)
