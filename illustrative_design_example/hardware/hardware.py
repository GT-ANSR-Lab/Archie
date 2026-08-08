from src.archie import *

# Hardware types
link_40g = Hardware("40GLink", DEVICE_TYPE.LINK)
link_40g.set_configuration("bandwidth", 40)
link_40g.set_configuration("cost", 10)

link_80g = Hardware("80GLink", DEVICE_TYPE.LINK)
link_80g.set_configuration("bandwidth", 80)
link_80g.set_configuration("cost", 40)

##### 
compute_4cores = Hardware("4Cores", DEVICE_TYPE.COMPUTE)
compute_4cores.set_entire_configuration({
    "cost": 100,
    "cores": 4,
    "NIC_Reorder_Buffer": 10
})

compute_8cores = Hardware("8Cores", DEVICE_TYPE.COMPUTE)
compute_8cores.set_entire_configuration({
    "cost": 250,
    "cores": 8,
    "NIC_Reorder_Buffer": 10
})

compute_16cores = Hardware("16Cores", DEVICE_TYPE.COMPUTE)
compute_16cores.set_entire_configuration({
    "cost": 700,
    "cores": 16,
    "NIC_Reorder_Buffer": 10
})

compute_4cores_lowfpga = Hardware("4Cores_lowFPGA", DEVICE_TYPE.COMPUTE)
compute_4cores_lowfpga.set_entire_configuration({
    "cost": 100,
    "cores": 4,
    "FPGA": True,
    "FPGA-capacity": 10,
    # "RDMA": True,
    "NIC_Reorder_Buffer": 20
})

compute_8cores_lowfpga = Hardware("8Cores_lowFPGA", DEVICE_TYPE.COMPUTE)
compute_8cores_lowfpga.set_entire_configuration({
    "cost": 300,
    "cores": 8,
    "FPGA": True,
    "FPGA-capacity": 10,
    # "RDMA": True,
    "NIC_Reorder_Buffer": 20
})

compute_16cores_lowfpga = Hardware("16Cores_lowFPGA", DEVICE_TYPE.COMPUTE)
compute_16cores_lowfpga.set_entire_configuration({
    "cost": 500,
    "cores": 16,
    "FPGA": True,
    "FPGA-capacity": 15,
    # "RDMA": True,
    "NIC_Reorder_Buffer": 20
})

compute_4cores_highfpga = Hardware("4Cores_highFPGA", DEVICE_TYPE.COMPUTE)
compute_4cores_highfpga.set_entire_configuration({
    "cost": 500,
    "cores": 4,
    "FPGA": True,
    "FPGA-capacity": 15,
    "RDMA": True,
    "NIC_TIMESTAMPS": True,
    "NIC_Reorder_Buffer": 20,
    # "SMART_NIC": True,
})

compute_8cores_highfpga = Hardware("16Cores_highFPGA", DEVICE_TYPE.COMPUTE)
compute_8cores_highfpga.set_entire_configuration({
    "cost": 1000,
    "cores": 16,
    "FPGA": True,
    "FPGA-capacity": 5,
    "RDMA": True,
    "NIC_TIMESTAMPS": True,
    "NIC_Reorder_Buffer": 20,
    "SMART_NIC": True,
})

compute_4cores_highreorder = Hardware("4Cores_HighReorder", DEVICE_TYPE.COMPUTE)
compute_4cores_highreorder.set_entire_configuration({
    "cost": 120,
    "cores": 4,
    "NIC_Reorder_Buffer": 50
})

compute_4cores_nitro = Hardware("4Cores_SmartNIC", DEVICE_TYPE.COMPUTE)
compute_4cores_nitro.set_entire_configuration({
    "cost": 150,
    "cores": 4,
    "NIC_TIMESTAMPS": True,
    "SMART_NIC": True,
    "NIC_Reorder_Buffer": 10
})

compute_8cores_nitro = Hardware("8Cores_SmartNIC", DEVICE_TYPE.COMPUTE)
compute_8cores_nitro.set_entire_configuration({
    "cost": 400,
    "cores": 8,
    "NIC_TIMESTAMPS": True,
    "SMART_NIC": True,
    "NIC_Reorder_Buffer": 10
})


compute_4cores_rdma = Hardware("4Cores_rdma", DEVICE_TYPE.COMPUTE)
compute_4cores_rdma.set_entire_configuration({
    "cost": 200,
    "cores": 4,
    "RDMA": True,
    "NIC_TIMESTAMPS": True,
    "NIC_Reorder_Buffer": 10
})

compute_8cores_rdma = Hardware("8Cores_rdma", DEVICE_TYPE.COMPUTE)
compute_8cores_rdma.set_entire_configuration({
    "cost": 420,
    "cores": 8,
    "RDMA": True,
    "NIC_TIMESTAMPS": True,
    "NIC_Reorder_Buffer": 20
})



############
router_2_qos_5_memory = Hardware("router_2qos_5memory", DEVICE_TYPE.ROUTER)
router_2_qos_5_memory.set_entire_configuration({
    "cost": 40,
    "QoS": 2,
    "memory": 5,
})

router_4_qos_10_memory_ecn = Hardware("router_4_qos_10_memory_ecn", DEVICE_TYPE.ROUTER)
router_4_qos_10_memory_ecn.set_entire_configuration({
    "cost": 65,
    "QoS": 4,
    "memory": 10,
    "ECN": True
})


router_8_qos_20_memory_ecn_int = Hardware("router_8_qos_20_memory_ecn_int", DEVICE_TYPE.ROUTER)
router_8_qos_20_memory_ecn_int.set_entire_configuration({
    "cost": 200,
    "QoS": 8,
    "memory": 20,
    "ECN": True,
    "INT": True
})

router_4_qos_10_memory_int = Hardware("router_4_qos_10_memory_int", DEVICE_TYPE.ROUTER)
router_4_qos_10_memory_int.set_entire_configuration({
    "cost": 80,
    "QoS": 4,
    "memory": 10,
    "ECN": True,
    "INT": True
})

router_16_qos_10_memory_ecn_int = Hardware("router_16_qos_10_memory_ecn_int", DEVICE_TYPE.ROUTER)
router_16_qos_10_memory_ecn_int.set_entire_configuration({
    "cost": 200,
    "QoS": 16,
    "memory": 10,
    "ECN": True,
    "INT": True
})

router_8_qos_20_memory_ecn_int = Hardware("router_8_qos_20_memory_ecn_int", DEVICE_TYPE.ROUTER)
router_8_qos_20_memory_ecn_int.set_entire_configuration({
    "cost": 200,
    "QoS": 8,
    "memory": 20,
    "ECN": True,
    "INT": True
})

router_tofino = Hardware("TofinoV1Router", DEVICE_TYPE.ROUTER)
router_tofino.set_entire_configuration({
    "cost": 300,
    "QoS": 8,
    "ECN": True,
    "INT": True,
    "P4": True,
    "P4-stages": 12,
    "memory": 10
})

router_tofino2 = Hardware("TofinoV2Router", DEVICE_TYPE.ROUTER)
router_tofino2.set_entire_configuration({
    "cost": 600,
    "QoS": 32,
    "ECN": True,
    "INT": True,
    "P4": True,
    "P4-stages": 20,
    "memory": 20
})

router_highcores = Hardware("router_highcores", DEVICE_TYPE.ROUTER)
router_highcores.set_entire_configuration({
    "cost": 600,
    "QoS": 32,
    "cores": 50,
    "ECN": True,
    "INT": True,
    "memory": 200
})