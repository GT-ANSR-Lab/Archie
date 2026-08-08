from src.archie import *

def link_upgrade(workload):
    links = workload.topology.get_children(device_type = DEVICE_TYPE.LINK)
    return And(*[link.configuration["bandwdith"] > 100 for link in links])

# LINK_UPGRADE = System("LinkUpgrade", MISC, link_upgrade)

# SuggestedOrdering("LINK_UPGRADE_th", throughput, LINK_UPGRADE, 5)
# SuggestedOrdering("LINK_UPGRADE_lat", latency, LINK_UPGRADE, 5)