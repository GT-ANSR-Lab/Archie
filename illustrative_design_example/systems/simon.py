from src.archie import *

def simon_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return Or(
        And(*[compute.configuration["SMART_NIC"] for compute in computes]),
        And(*[And(compute.configuration["FPGA"], compute.constrained_slots["FPGA-capacity"]["SIMON"] == 10) for compute in computes]),
    )

SIMON = System("SIMON", monitor, simon_apply)