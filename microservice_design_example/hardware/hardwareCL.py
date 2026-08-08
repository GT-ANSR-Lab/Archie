from src.archie import *

# CloudLab Wisconsin c220g1: Cisco UCS C220 M4 SFF
# Optimized for balanced compute and storage workloads.
c220g1 = Hardware("c220g1-cloudlab", DEVICE_TYPE.COMPUTE)
c220g1.set_entire_configuration({
    "cores": 16,                         # 2 x Intel E5-2630 v3 (8 cores each)
    "memory_GB": 128,                    # 128 GB ECC RAM
    "storage_GB": 2880,                  # 1x 480GB SSD + 2x 1.2TB HDD
    "network_bandwidth_Gbps": 10,        # Dual-port 10Gb SFP+
    "virtualization_support": "VT-x/VT-d", # Relevant for Knative/VM-based runtimes
    "arch": "x86_64"
})

# CloudLab Wisconsin c220g2: Cisco UCS C220 M4 SFF (Higher Core/Memory)
# Optimized for higher density microservice deployments and service meshes.
c220g2 = Hardware("c220g2-cloudlab", DEVICE_TYPE.COMPUTE)
c220g2.set_entire_configuration({
    "cores": 20,                         # 2 x Intel E5-2660 v3 (10 cores each)
    "memory_GB": 160,                    # 160 GB ECC RAM
    "storage_GB": 2880,                  # 1x 480GB SSD + 2x 1.2TB HDD
    "network_bandwidth_Gbps": 10,        # Dual-port 10Gb SFP+
    "virtualization_support": "VT-x/VT-d",
    "arch": "x86_64"
})