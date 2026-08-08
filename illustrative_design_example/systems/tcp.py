from src.archie import *

def tcp_apply(workload):
    return BoolVal(True)

TCP = System("TCP", transport, tcp_apply, objectives = [latency, throughput, ease_of_deployment])