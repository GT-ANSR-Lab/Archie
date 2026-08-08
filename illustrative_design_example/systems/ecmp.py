from src.archie import *

def ecmp_apply(workload):
    return BoolVal(True)

ECMP = System("ECMP", load_balancer, ecmp_apply, objectives = [load_balancing])