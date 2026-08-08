from src.archie import *

# Systems
def rdma_apply(workload):
    computes = workload.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
    return And(
        And(*[compute.configuration["RDMA"] for compute in computes]),
    )

RDMA = System("RDMA", transport, rdma_apply, objectives = [latency, throughput, ease_of_deployment])
# RDMA.add_warning(lambda workload: workload.topology.properties["CyclicBufferDep"], "RDMA can run into black holes in the presence of cyclic buffer dependencies.")

# SuggestedOrdering("RDMA_loss", loss_less, RDMA, 10)

# SuggestedOrdering("RDMA_ease_of_deployment", ease_of_deployment, RDMA, 5, lambda workload: And(workload.solutions["TCP"], Not(workload.solutions["eqds"])))
# SuggestedOrdering("RDMA_ease_of_deployment", ease_of_deployment, RDMA, 10, lambda workload: And(workload.solutions["TCP"], workload.solutions["eqds"]))