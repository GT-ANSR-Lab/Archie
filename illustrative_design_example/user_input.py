from src.archie import *
from src.systems_import import *
from hardware.hardware import *
from systems.orderings import *

import user_topology

import sys

def main():

    # Required to explain
    explain_req = ""

    # Check if an explain request is provided
    if len(sys.argv) > 1:
        explain_req = sys.argv[1]

    # Creating a topology
    pod = user_topology.create_topology()
    racks = pod.get_children(devicegroup_type = DEVICEGROUP_TYPE.RACK)

    # WORKLOAD 1
    ML_Training_Workload = Workload("ML_Training", 
                                    racks[0], 
                                    [dc_flows, long_flows, ml_training], 
                                    [latency, throughput, ease_of_deployment, monitoring], 
                                    )
    
    Optimize(ML_Training_Workload, latency, 1)
    Optimize(ML_Training_Workload, throughput, 2)
    Optimize(ML_Training_Workload, ease_of_deployment, 3)
    Optimize(ML_Training_Workload, monitoring, 4)


    # WORKLOAD 2
    # FrontEnd_Workload = Workload("FrontEnd", racks[0], [internet_flows, high_priority, long_flows], [latency, throughput, fairness, security, fault_tolerance, application_modification, ease_of_deployment], compute_load=10 ,network_load=20)
    # Optimize(FrontEnd_Workload, latency, 1)
    # Optimize(FrontEnd_Workload, application_modification, 2)
    # Optimize(FrontEnd_Workload, monitoring, 3)

    add_topology_constraints(SOLVER)
    print(DEVICES)
    evaluate(debug=True, explain="")

    print("###########################")
    if bool(explain_req):
        print("EXPLAINING")
        explain("ML_Training", "load_balancer", "latency")
        # explain("ML_Training", "virtual_switch", "ease_of_deployment", fix_roles=[])


if __name__ == "__main__":
    main()