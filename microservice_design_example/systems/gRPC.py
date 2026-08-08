from src.archie import *
 


def grpc_apply(workload):

    grpc_enabled = workload.solutions.get("gRPC", BoolVal(False))

    if ease_of_deployment in workload.objectives:
        if latency in workload.objectives and OPTIMIZERS["ease_of_deployment"].priority < OPTIMIZERS["latency"].priority and go not in workload.properties:
            track = f"gRPC is unavailable when ease of deployment and latency are objectives without Go implicit multi-threading programming language support"
            constraint = Implies(grpc_enabled, BoolVal(False))
            SOLVER.assert_and_track(constraint, track)
            TRACKED_CONSTRAINTS[track] = constraint

    if high_load in workload.properties and latency in workload.objectives and OPTIMIZERS["latency"].priority < OPTIMIZERS["ease_of_deployment"].priority:
        track = f"gRPC requires Asynchronous configuration when high load is a workload property and latency is an objective as it is not bottlenecked by timing of synchronous calls"
        constraint = Implies(grpc_enabled, (workload.solution_configs["gRPC"]["Asynchronous"]))
        SOLVER.assert_and_track(constraint, track)
        TRACKED_CONSTRAINTS[track] = constraint

    return BoolVal(True)


gRPC = System(
    "gRPC",
    rpc,
    grpc_apply,
    configs=["Synchronous", "Asynchronous"],
)
