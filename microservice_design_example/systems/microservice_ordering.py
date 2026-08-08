from src.archie import *
from src.systems_import import *

# Latency ordering
Ordering(latency, CRIO, same_as = Containerd)
Ordering(latency, Containerd, better_than = Docker)

Ordering(latency, Kubernetes_orchestrator, same_as = DockerSwarm)
Ordering(latency, Knative, same_as = Kubernetes_orchestrator)

Ordering(latency, Kubernetes_autoscaler, same_as = KEDA)

Ordering(latency, Istio, better_than = Linkerd)

Ordering(latency, gRPC, better_than = Thrift)


# Ease of deployment ordering
Ordering(ease_of_deployment, Docker, same_as = Containerd)
Ordering(ease_of_deployment, Containerd, better_than = CRIO)

Ordering(ease_of_deployment, Kubernetes_orchestrator, same_as = DockerSwarm)
Ordering(ease_of_deployment, Knative, same_as = Kubernetes_orchestrator)

Ordering(ease_of_deployment, Kubernetes_autoscaler, same_as = KEDA)

Ordering(ease_of_deployment, Istio, same_as = Linkerd)

Ordering(ease_of_deployment, gRPC, better_than = Thrift)

