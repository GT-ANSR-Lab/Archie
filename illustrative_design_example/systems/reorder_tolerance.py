from src.archie import *

# Systems
def reorder_tolerance_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    dcs = workload.topology.get_parents(devicegroup_type = DEVICEGROUP_TYPE.DC)
    dc_reordering = dcs[0].devicegroup_properties["Reordering"]
    return And(
        And(*[Or(compute.configuration["NIC_Reorder_Buffer"] >= dc_reordering, And(compute.configuration["NIC_loss_recovery_fancy?"], workload.solutions["BBR"])) for compute in computes]),
    )

# Reorder_Tolerance = System("Reorder_Tolerance", MISC, reorder_tolerance_apply)
