# Archie: Lightweight Design and Verification tool for System Architects

This directory is the submitted, runnable Archie microservice-design case study.  It models a ten-node, two-rack pod; CloudLab compute hardware; and design choices across container runtimes, orchestration, service meshes, RPC frameworks, and autoscaling.  Archie converts these choices and their compatibility rules into a Z3 optimization problem, maximizing the workload’s ease of deployment and latency objectives while checking all registered constraints.  An optional explanation mode reports why conflicting choices cannot coexist.
## Contents

| Path | Files and purpose |
| --- | --- |
| [`src/archie.py`](src/archie.py) | Self-contained copy of Archie’s core modeling, optimization, result-reporting, and explanation engine. |
| [`hardware/hardwareCL.py`](hardware/hardwareCL.py) | Declares the CloudLab Wisconsin `c220g1` and `c220g2` compute profiles used as candidate hardware. |
| [`input/user_topology.py`](input/user_topology.py) | Builds the two-rack pod with ten compute nodes. |
| [`input/user_input.py`](input/user_input.py) | Defines the Microservice workload with properties and objectives, calls the solver, and enables explanation mode when an argument is supplied. |
| [`systems/CRIO.py`](systems/CRIO.py), [`systems/Containerd.py`](systems/Containerd.py), [`systems/Docker.py`](systems/Docker.py) | Container-runtime systems. |
| [`systems/DockerSwarm.py`](systems/DockerSwarm.py), [`systems/KubernetesOrchestrator.py`](systems/KubernetesOrchestrator.py), [`systems/Knative.py`](systems/Knative.py) | Orchestrator systems. |
| [`systems/Istio.py`](systems/Istio.py), [`systems/Linkerd.py`](systems/Linkerd.py) | Service-mesh systems. |
| [`systems/gRPC.py`](systems/gRPC.py), [`systems/Thrift.py`](systems/Thrift.py) | RPC-framework systems. |
| [`systems/KEDA.py`](systems/KEDA.py), [`systems/KubernetesAutoscaler.py`](systems/KubernetesAutoscaler.py) | Autoscaler systems. |
| [`systems/microservice_ordering.py`](systems/microservice_ordering.py) | Imports every policy and declares relative ordering for latency and ease of deployment. |
| `output/` | Optional case-study-local destination for generated reports; it intentionally has no README. |
| [`README.md`](README.md) | This case-study guide. |

## Run and save results

Use the commands below from the repository root (not from this subdirectory). 

In order to replicate the findings of the paper, please note that the priority numbers in user_input.py needs to be correctly provided for the Optimize constraints: lower priority the better. So for example,
```bash
Optimize(ease_of_deployment, 1)
Optimize(latency, 2)
```
prioritizes ease_of_deployment over latency.

### Linux and macOS/Unix (Highly Recommended)

```bash
unset PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
python3 user_input.py > output/microservice_design.txt
```

If constraint explanations are intended:
```bash
unset PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
python3 user_input.py explain > output/microservice_design.txt
```

### Windows (PowerShell) (Not Tested and unverified)

```powershell
New-Item -ItemType Directory -Force output | Out-Null
Remove-Item Env:\PYTHONPATH
$env:PYTHONPATH = "."
py > output\design.txt 2>&1
py explain > output\microservice_design_explain.txt 2>&1
```
If constraint explanations are intended:
```powershell
New-Item -ItemType Directory -Force output | Out-Null
Remove-Item Env:\PYTHONPATH
$env:PYTHONPATH = "."
py explain > output\microservice_design_explain.txt 2>&1
```

## Explanation Framework
The definition of explain function is:
```python
explain(workload, order_role, order_objective, fix_hardware=None, fix_roles=None, solver=SOLVER)
```
The required arguments are **workload**, which is relevant when there are more than 1 workloads, **order_role**, to determine which role's ordering to check, **order_objective** to also determine which ordering to check.
The optional arguments are **fix_hardware**, which if None (by default) allows all hardware to be flexible when considering to enable the non-chosen higher priority system, "all" which means the hardware choices are fixed and cannot be changed when trying to enable to non-chosen higher priority system, or a list that contains a subset of hardware choices to fix. For fix_roles, it takes None (by default) which _fixes_ all the systems chosen for the other roles, or a list containing a subset of roles to be fixed while trying to enable non-chosen higher priority system. 


Read the standard report at [`../output/microservice_design.txt`](../output/microservice_design.txt) and the explanation report at [`../output/microservice_design_explain.txt`](../output/microservice_design_explain.txt).  The first command is sufficient for normal reproduction; the second is for inspecting constraint explanations.
