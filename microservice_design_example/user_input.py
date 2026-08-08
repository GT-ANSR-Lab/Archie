from src.archie import *
from src.systems_import import *
from hardware.hardwareCL import *
from systems.microservice_ordering import *

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


    Microservice_Workload = Workload("Microservice", pod, 
                                     properties=[heterogenous, medium_load, application_observability, go, l7_load_balancing], 
                                     objectives=[ease_of_deployment, latency])
    Optimize(Microservice_Workload, latency, 2)
    Optimize(Microservice_Workload, ease_of_deployment, 1)

    add_topology_constraints(SOLVER)
    evaluate(debug=True, explain="")
    print("###########################")
    if bool(explain_req):
        print("EXPLAINING")
        explain("Microservice", "Service mesh", "latency", fix_roles=[])

if __name__ == "__main__":
    main()
