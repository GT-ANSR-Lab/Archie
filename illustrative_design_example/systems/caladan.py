from src.archie import *

def caladan_apply(workload):
    if match_subset(workload.objectives, [host_resource_isolation]):
        return workload.solutions["shenango"] 
    else:
        caladan_False = Bool("caladan_objective_isolation")
        VAR_DESCRIPTIONS["caladan_objective_isolation"] = "Host Resource Isolation objective for Caladan"
        SOLVER.assert_and_track(caladan_False == BoolVal(False), "track_caladan_no_objective_isolation")
        TRACKED_CONSTRAINTS["track_caladan_no_objective_isolation"] = (caladan_False == BoolVal(False))
        return caladan_False

CALADAN = System("Caladan", cpu_sched, caladan_apply)