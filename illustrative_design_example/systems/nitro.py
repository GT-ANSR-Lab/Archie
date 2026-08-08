from src.archie import *

def NITRO_apply(workload):
    if dc_flows in workload.properties:
        computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
        constraints = And(
            And(*[compute.configuration["SMART_NIC"] for compute in computes])
        )
        return Implies(WORKLOAD_PROPERTIES[dc_flows.id], constraints)
    else:
        nitro_False = Bool("nitro_dc_flows")
        VAR_DESCRIPTIONS["nitro_dc_flows"] = "DC flows present for NITRO"
        SOLVER.assert_and_track(nitro_False == BoolVal(False), "track_nitro_no_dc_flows")
        TRACKED_CONSTRAINTS["track_nitro_no_dc_flows"] = (nitro_False == False)
        return nitro_False

NITRO = System("NITRO", virtual_switch, NITRO_apply, objectives = [ease_of_deployment])