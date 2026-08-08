# Archie: Lightweight Design and Verification tool for System Architects

This directory is the submitted, runnable Archie illustrative-design case study. It models a pod topology, available hardware, and design choices across network systems and protocols. Archie converts these choices and their compatibility rules into a Z3 optimization problem, maximizing the workload objectives while checking all registered constraints. An optional explanation mode reports why conflicting choices cannot coexist.

Verify the environment with `python3 -c 'import z3; print(z3.get_version_string())'` on Unix or `py -c "import z3; print(z3.get_version_string())"` on Windows. It must report Z3 4.13.0 or later.

## Contents

| Path | Files and purpose |
| --- | --- |
| [`src/archie.py`](src/archie.py) | Self-contained copy of Archie’s core modeling, optimization, result-reporting, and explanation engine. |
| [`hardware/hardware.py`](hardware/hardware.py) | Declares the candidate hardware profiles used by the case study. |
| [`user_topology.py`](user_topology.py) | Builds the illustrative topology. |
| [`user_input.py`](user_input.py) | Defines the workloads with its properties and objectives, calls the solver, and enables explanation mode when an argument is supplied. |
| [`systems/`](systems/) | System-policy definitions and [`systems/orderings.py`](systems/orderings.py), which declares relative ordering for objectives. |
| [`output/`](output/) | Optional case-study-local destination for generated reports. |
| [`README.md`](README.md) | This case-study guide. |

## Run and save results

Use the commands below from this directory. They import the system ordering definitions so that the policy registry is complete, then execute `user_input.main()`. Standard output and errors are redirected to the local [`output/`](output/) directory.

In order to replicate the findings of the paper, please note that the priority numbers in `user_input.py` need to be correctly provided for the `Optimize` constraints: lower priority is better. For example,

```python
Optimize(ease_of_deployment, 1)
Optimize(latency, 2)
```

prioritizes `ease_of_deployment` over `latency`.

### Linux and macOS/Unix (Highly Recommended)

```bash
unset PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
python3 user_input.py > output/illustrative_design.txt
```

To replicate the paper’s **single-workload** example, run the command with `explain`; the output will include the explanation report:

```bash
unset PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
python3 user_input.py explain > output/illustrative_design_explain.txt
```

### Windows (PowerShell) (Not Tested and unverified)

```powershell
New-Item -ItemType Directory -Force output | Out-Null
Remove-Item Env:\PYTHONPATH
$env:PYTHONPATH = "."
py user_input.py > output\illustrative_design.txt 2>&1
```

To include constraint explanations:

```powershell
New-Item -ItemType Directory -Force output | Out-Null
Remove-Item Env:\PYTHONPATH
$env:PYTHONPATH = "."
py user_input.py explain > output\illustrative_design_explain.txt 2>&1
```

Read the standard report at [`output/illustrative_design.txt`](output/illustrative_design.txt) and the explanation report at [`output/illustrative_design_explain.txt`](output/illustrative_design_explain.txt). The first command is sufficient for normal reproduction; the second is for inspecting constraint explanations.

## Replicate the additional-workload example

To replicate the paper’s **additional-workload** example, edit [`user_input.py`](user_input.py) as follows:

1. Uncomment the `FrontEnd_Workload` definition and its three `Optimize` calls on lines 37–40.
2. Comment out the `explain(...)` call on line 49 and uncomment the alternative `explain(...)` call on line 50.

Update the [`systems/orderings.py`](systems/orderings.py) by commenting out 80 and 81 (the first 2 lines of Orderings in the Virtual Switch) and uncommenting lines 82 and 83 (the second 2 lines of Orderings in the Virtual Switch).

3. Finally, run the explanation command above.

## Explanation Framework
The definition of explain function is:
```python
explain(workload, order_role, order_objective, fix_hardware=None, fix_roles=None, solver=SOLVER)
```
The required arguments are **workload**, which is relevant when there are more than 1 workloads, **order_role**, to determine which role's ordering to check, **order_objective** to also determine which ordering to check.
The optional arguments are **fix_hardware**, which if None (by default) allows all hardware to be flexible when considering to enable the non-chosen higher priority system, "all" which means the hardware choices are fixed and cannot be changed when trying to enable to non-chosen higher priority system, or a list that contains a subset of hardware choices to fix. For fix_roles, it takes None (by default) which _fixes_ all the systems chosen for the other roles, or a list containing a subset of roles to be fixed while trying to enable non-chosen higher priority system. 

## Explainability and system constraints format

Rather than using `assert_and_track` for every constraint, this case study includes objectives and workload properties as Boolean variables in the solver. Each variable has a description, which is displayed in the explanation output to make the relevant system constraints easier to understand.

The eventual goal is for Archie to sit behind a seamless LLM interface that can parse inputs and outputs and reliably translate them into Python code. Consequently, the current output is not yet completely descriptive or presented in the most intuitive form.

## Caveat

Due to variance in hardware costs and inventory changes—the inventory was constantly updated based on gathered information and observations—the cost and appendix results are not provided. The template used was otherwise exactly the same.
