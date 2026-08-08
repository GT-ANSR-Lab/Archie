from src.archie import *

def SRD_CCA_apply(workload):
    return workload.solutions["SRD"]

SRD_CCA = System("SRD_CCA", cca, SRD_CCA_apply)

# SuggestedOrdering("SRD_CCA_th", throughput, SRD_CCA, 1)
# SuggestedOrdering("SRD_CCA_lat", latency, SRD_CCA, 1)

# SuggestedOrdering("SRD_CCA_multiten", multi_tenancy, SRD_CCA, 1)
# SuggestedOrdering("SRD_CCA_sec", security, SRD_CCA, 1)
# SuggestedOrdering("SRD_CCA_isol", isolation, SRD_CCA, 1)