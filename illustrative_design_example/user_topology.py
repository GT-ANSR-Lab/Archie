from src.archie import *

def create_topology():
    return create_microservice_pod("pod1", num_racks=2, num_routers=1, num_cpus=7)