from src.archie import *
 


def thrift_apply(workload):

    thrift_enabled = workload.solutions.get("Thrift", BoolVal(False))

    if latency in workload.objectives:
        track = f"Thrift requires the binary configuration when latency is an objective"
        constraint = Implies(thrift_enabled, workload.solution_configs["Thrift"]["binary"])
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

        if ease_of_deployment in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and not go in workload.properties:
            track = f"Thrift is unavailable when latency and ease of deployment are objectives without Go implicit multi-threading support"
            constraint = Implies(thrift_enabled, BoolVal(False))
            SOLVER.assert_and_track(constraint, track)
            TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


Thrift = System(
    "Thrift",
    rpc,
    thrift_apply,
    objectives=[latency, ease_of_deployment],
    configs=["text-based", "binary"]
)
