from src.archie import *
from src.systems_import import *

# CPU Schedulers

Ordering(host_resource_isolation, SHENANGO, better_than = LINUX)
Ordering(host_resource_isolation, ZYGOS, same_as = SHENANGO)
Ordering(host_resource_isolation, LINUX, same_as = NETCHANNEL)
Ordering(host_resource_isolation, LINUX, same_as = SNAP)
Ordering(host_resource_isolation, SNAP, better_than = DEMIKERNEL)


Ordering(throughput, NETCHANNEL, better_than = LINUX)
Ordering(throughput, ZYGOS, better_than = LINUX)
Ordering(throughput, SHENANGO, better_than = LINUX)
Ordering(throughput, DEMIKERNEL, better_than = LINUX)
Ordering(throughput, SNAP, better_than = LINUX)
Ordering(throughput, DEMIKERNEL, same_as = SNAP, condition = lambda workload: workload.solution_configs["snap"]["PONY"])
Ordering(throughput, DEMIKERNEL, same_as = LINUX, condition = lambda workload: workload.solution_configs["snap"]["LINUX"])

Ordering(ease_of_deployment, LINUX, better_than = SNAP)
Ordering(ease_of_deployment, NETCHANNEL, same_as = LINUX)
Ordering(ease_of_deployment, SNAP, better_than = SHENANGO)
Ordering(ease_of_deployment, DEMIKERNEL, same_as = SHENANGO, condition = lambda workload: Not(workload.solutions["RDMA"]))
Ordering(ease_of_deployment, DEMIKERNEL, same_as = LINUX, condition = lambda workload: workload.solutions["RDMA"])
Ordering(ease_of_deployment, SHENANGO, better_than = ZYGOS)




# Ordering of CPU schedulers for application modification
Ordering(application_modification, LINUX, better_than = SNAP, condition = lambda workload: workload.solution_configs["snap"]["PONY"])
Ordering(application_modification, LINUX, same_as = SNAP, condition = lambda workload: workload.solution_configs["snap"]["LINUX"])
Ordering(application_modification, NETCHANNEL, same_as = LINUX)
Ordering(application_modification, SNAP, better_than = SHENANGO)
Ordering(application_modification, SHENANGO, same_as = DEMIKERNEL)
Ordering(application_modification, SHENANGO, same_as = ZYGOS)

# Ordering of CPU schedulers for latency
Ordering(latency, ZYGOS, better_than = SHENANGO)
Ordering(latency, SHENANGO, same_as = DEMIKERNEL)
Ordering(latency, SHENANGO, better_than = SNAP)
Ordering(latency, ZYGOS, better_than = SNAP)
Ordering(latency, SNAP, better_than = LINUX, condition = lambda workload: And(*[link.configuration["bandwidth"] >= 40 for link in workload.topology.get_children(device_type = DEVICE_TYPE.LINK)]))
Ordering(latency, LINUX, same_as = ZYGOS, condition = lambda workload: And(*[link.configuration["bandwidth"] < 40 for link in workload.topology.get_children(device_type = DEVICE_TYPE.LINK)]))
Ordering(latency, LINUX, same_as = NETCHANNEL)

# Ordering of CPU schedulers for compute efficiency
Ordering(compute_efficiency, SHENANGO, same_as = DEMIKERNEL)
Ordering(compute_efficiency, SHENANGO, better_than = SNAP)
Ordering(compute_efficiency, SNAP, better_than = LINUX)
Ordering(compute_efficiency, LINUX, better_than = ZYGOS)
Ordering(compute_efficiency, LINUX, better_than = NETCHANNEL)

# CCA
Ordering(latency, BFC, better_than = DCQCN)
Ordering(latency, DCQCN, better_than = TIMELY)
Ordering(latency, DCTCP, same_as = TIMELY)
Ordering(latency, TIMELY, better_than = BBR)
Ordering(latency, BBR, better_than = CUBIC)

Ordering(throughput, DCQCN, same_as = BFC)
Ordering(throughput, DCQCN, same_as = TIMELY)
Ordering(throughput, DCQCN, same_as = DCTCP)
Ordering(throughput, DCQCN, same_as = BBR)
Ordering(throughput, DCQCN, better_than = CUBIC)


Ordering(fairness, BFC, better_than = DCTCP)
Ordering(fairness, DCTCP, better_than = DCQCN)
Ordering(fairness, DCQCN, better_than = CUBIC)
Ordering(fairness, CUBIC, better_than = BBR)
Ordering(fairness, CUBIC, better_than = TIMELY)

Ordering(scavenger, LEDBAT, exact_value = 10)

# Virtual Switch

# Ordering of Virtual Switches for ease of deployment
Ordering(ease_of_deployment, ANDROMEDA, better_than = VFP)
Ordering(ease_of_deployment, ANDROMEDA, better_than = NITRO)
# Ordering(ease_of_deployment, VFP, better_than = ANDROMEDA)
# Ordering(ease_of_deployment, ANDROMEDA, better_than = NITRO)

# Transport

Ordering(latency, RDMA, same_as = SRD)
Ordering(latency, RDMA, better_than = PONY)
Ordering(latency, PONY, better_than = TCP)

Ordering(throughput, RDMA, same_as = SRD) 
Ordering(throughput, RDMA, same_as = PONY) 
Ordering(throughput, RDMA, better_than = TCP) 

Ordering(ease_of_deployment, TCP, better_than = RDMA)
Ordering(ease_of_deployment, RDMA, better_than = SRD)
Ordering(ease_of_deployment, RDMA, same_as = PONY)


Ordering(application_modification, TCP, better_than = RDMA)
Ordering(application_modification, RDMA, same_as = PONY)
Ordering(application_modification, RDMA, better_than = SRD)

# Load Balancing

Ordering(load_balancing, PACKETSPRAY, better_than = CONGA)
Ordering(load_balancing, CONGA, same_as = PLB)
Ordering(load_balancing, PLB, better_than = ECMP)



Ordering(latency, PACKETSPRAY, better_than = CONGA)
Ordering(latency, CONGA, better_than = ECMP)
Ordering(latency, CONGA, same_as = PLB)

Ordering(ease_of_deployment, PLB, better_than = CONGA)
Ordering(ease_of_deployment, ECMP, better_than = CONGA)
Ordering(ease_of_deployment, PACKETSPRAY, better_than = CONGA)
Ordering(ease_of_deployment, ECMP, better_than = PACKETSPRAY)


# Monitoring

Ordering(monitoring, SONATA, better_than = SIMON)
Ordering(monitoring, SIMON, better_than = PINGMESH)
    
    