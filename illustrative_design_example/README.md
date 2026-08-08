# Archie: Lightweight Design and Verification tool for System Architects

This directory is the submitted, runnable Archie illustrative-design case study. It models a pod topology, available hardware, and design choices across network systems and protocols. Archie converts these choices and their compatibility rules into a Z3 optimization problem, maximizing the workload objectives while checking all registered constraints. An optional explanation mode reports why conflicting choices cannot coexist.

## Prerequisites

Run with **Python 3.11.5 or later** and **Z3 4.13.0 or later**. Install Z3’s Python bindings, which include the required solver library:

```bash
# Linux/macOS/Unix, from the repository root
python3 -m pip install "z3-solver>=4.13.0"
```

```powershell
# Windows PowerShell, from the repository root
py -m pip install "z3-solver>=4.13.0"
```

Verify the environment with `python -c 'import z3; print(z3.get_version_string())'` on Unix or `py -c "import z3; print(z3.get_version_string())"` on Windows. It must report Z3 4.13.0 or later.

## Contents

| Path | Files and purpose |
| --- | --- |
| [`src/archie.py`](src/archie.py) | Self-contained copy of Archie’s core modeling, optimization, result-reporting, and explanation engine. |
| [`hardware/hardware.py`](hardware/hardware.py) | Declares the candidate hardware profiles used by the case study. |
| [`user_topology.py`](user_topology.py) | Builds the illustrative topology. |
| [`user_input.py`](user_input.py) | Defines the workloads and objectives, calls the solver, and enables explanation mode when an argument is supplied. |
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
python3 user_input.py > output/illustrative_design.txt 2>&1
```

To replicate the paper’s **single-workload** example, run the command with `explain`; the output will include the explanation report:

```bash
unset PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
python3 user_input.py explain > output/illustrative_design_explain.txt 2>&1
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
3. Run the explanation command above.

## Explainability and system constraints

Rather than using `assert_and_track` for every constraint, this case study includes objectives and workload properties as Boolean variables in the solver. Each variable has a description, which is displayed in the explanation output to make the relevant system constraints easier to understand.

The eventual goal is for Archie to sit behind a seamless LLM interface that can parse inputs and outputs and reliably translate them into Python code. Consequently, the current output is not yet completely descriptive or presented in the most intuitive form.

## Caveat

Due to variance in hardware costs and inventory changes—the inventory was constantly updated based on gathered information and observations—the cost and appendix results are not provided. The template used was otherwise exactly the same.
