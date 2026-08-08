from z3 import *
import time
from collections import defaultdict
from enum import Enum
from itertools import chain
from pprint import pprint

HARDWARES = defaultdict(list)
HARDWARE_CONFIGURATIONS = {}

CONSTRAINED_SLOTS = defaultdict(dict)
EXCLUSIVE_SLOTS = defaultdict(dict)

DEVICES = {}
DEVICE_PROPERTIES = {}

DEVICEGROUPS = {}
DEVICEGROUP_PROPERTIES = {}

WORKLOAD_PROPERTIES = {}
OBJECTIVES = {}
WORKLOADS = {}
ROLES = {}
SYSTEMS = {}
ORDERINGS = []
SUGGESTED_ORDERINGS = []
OPTIMIZERS = {}
EXPLAIN_OPTIMIZERS = []

# Added for Explainability
TRACKED_CONSTRAINTS = {}
ASSIGNMENT_DICT = {}
VAR_DESCRIPTIONS = {}
HARDWARE_ID_MAPPING = {}
ALL_PROPERTIES = []
ALL_OBJECTIVES = []

TOTAL_COST = Real("Total cost")
VAR_DESCRIPTIONS["Total cost"] = "Total cost"
PERFORMANCE = Real("Total reward")
VAR_DESCRIPTIONS["Total reward"] = "Total performance reward"

SOLVER = Optimize()
SOLVER_UNSAT = Optimize()
SOLVER_UNSAT_FINE = Optimize()
WARNINGS = False

HARDWARE_VARIABLES_SUFFIX = "_hardware_id"

counter = 0

def get_id(*args):
    args = [str(arg) for arg in args]
    return "_".join(args)


class DEVICEGROUP_TYPE(Enum):
    ATOMIC = 0
    RACK = 1
    POD = 2
    DC = 3


class DEVICE_TYPE(Enum):
    ROUTER = 0
    LINK = 1
    COMPUTE = 2
    STORAGE = 3

class FIBRE_TYPE(Enum):
    ETHERNET = 0
    INFINIBAND = 1


class DeviceGroupProperties:
    def __init__(self, devicegroup_type):
        self.id = devicegroup_type
        self.properties = {}
        DEVICEGROUP_PROPERTIES[devicegroup_type] = self
    
    def add_property(self, key, value=None):
        self.properties[key] = value


class DeviceGroup:
    def __init__(self, id, devicegroup_type = None):
        self.id = id
        if id in DEVICEGROUPS:
            raise KeyError("Creating a device group of " + str(id) + " but it already exists.")

        self.devicegroup_type = devicegroup_type
        self.parents = []
        self.children = []
        self.workloads = []
        if devicegroup_type in DEVICEGROUP_PROPERTIES:
            self.devicegroup_properties = DEVICEGROUP_PROPERTIES[devicegroup_type].properties
        else:
            self.devicegroup_properties = {}
        DEVICEGROUPS[id] = self

    def add_workload(self, workload):
        self.workloads.append(workload)
        for child in self.children:
            child.add_workload(workload)
    
    def add_children(self, children):
        self.children += children
        for child in children:
            child.add_parent(self)
    
    def add_parent(self, parent):
        self.parents.append(parent)

    def get_children(self, devicegroup_type = None, device_type = None):
        # print(self.children)
        if devicegroup_type == None:
            devicegroup_type = DEVICEGROUP_TYPE.ATOMIC

        children = []
        for child in self.children:
            if child.devicegroup_type == devicegroup_type:
                if device_type == None or child.device_type == device_type:
                    children.append(child)
            children += child.get_children(devicegroup_type, device_type)
        return children

    def get_parents(self, devicegroup_type = None):
        parents = []
        for parent in self.parents:
            if parent.devicegroup_type == devicegroup_type:
                parents.append(parent)
            parents += parent.get_parents(devicegroup_type)
        return parents
    
    def set_property(self, key, value):
        self.devicegroup_properties[key] = value


class DeviceProperties:
    def __init__(self, device_type):
        self.id = device_type
        self.properties = {}
        DEVICE_PROPERTIES[device_type] = self
    
    def add_property(self, key, value=None):
        self.properties[key] = value


class HardwareConfiguration:
    def __init__(self, hardware_type):
        if hardware_type in HARDWARE_CONFIGURATIONS:
            raise KeyError("Hardware configuration already exists for - " + str(hardware_type))

        self.configuration = {}
        self.default_value = {}
        HARDWARE_CONFIGURATIONS[hardware_type] = self
    
    def add_configuration(self, config_id, config_type, default_value):
        self.configuration[config_id] = config_type
        self.default_value[config_id] = default_value


class Hardware:
    def __init__(self, id, hardware_type):
        if hardware_type not in HARDWARE_CONFIGURATIONS:
            raise KeyError("Hardware configuration does not exist for hardware type - " + str(hardware_type))

        self.id = id
        self.index = len(HARDWARES[hardware_type])
        self.hardware_type = hardware_type
        HARDWARES[hardware_type].append(self)
        self.configuration = {}
        if hardware_type not in HARDWARE_ID_MAPPING:
            HARDWARE_ID_MAPPING[hardware_type] = {}
        HARDWARE_ID_MAPPING[hardware_type][self.id] = self.index

    def set_configuration(self, key, config_value):
        self.configuration[key] = config_value
    
    def set_entire_configuration(self, config):
        for key in config:
            self.set_configuration(key, config[key])

    def get_configuration(self, key, default_value):
        if key not in self.configuration.keys():
            return default_value
        return self.configuration[key]
    
    def get_constraints(self, device_configuration):
        for key in HARDWARE_CONFIGURATIONS[self.hardware_type].configuration:
            if key not in self.configuration:
                self.configuration[key] = HARDWARE_CONFIGURATIONS[self.hardware_type].default_value[key]
                if WARNINGS:
                    print("Warning: Configuration for " + str(self.id) + " is missing " + str(key) + ". Using default values.")

        constraints = []
        for key in self.configuration:
            constraints.append(device_configuration[key] == self.configuration[key])

        return And(*constraints)


class ConstrainedSlot:
    def __init__(self, id, device_type, universe = [SYSTEMS, WORKLOADS]):
        self.id = id
        CONSTRAINED_SLOTS[device_type][id] = self
        self.universe = universe
        HARDWARE_CONFIGURATIONS[device_type].add_configuration(id, Real, 0)

class ExclusiveSlot:
    def __init__(self, id, device_type, universe = None):
        if universe == None:
            universe = HARDWARES[device_type]
        self.id = id

class Device(DeviceGroup):
    def __init__(self, id, device_type, hardware=None):
        id = id + "_" + str(device_type)
        if id in DEVICES:
            raise KeyError("Creating a device of " + str(id) + " but it already exists.")

        super().__init__(id, DEVICEGROUP_TYPE.ATOMIC)
        self.device_type = device_type
        self.constraints = BoolVal(True)
        self.configuration = {}
        self.device_properties = DEVICE_PROPERTIES[device_type].properties

        hardware_config = HARDWARE_CONFIGURATIONS[device_type].configuration
        for key in hardware_config:
            self.configuration[key] = hardware_config[key](id + "_" + key)

        DEVICES[id] = self
        self.hardware_id = Real(self.id + HARDWARE_VARIABLES_SUFFIX)
        VAR_DESCRIPTIONS[self.id + HARDWARE_VARIABLES_SUFFIX] = "Hardware ID for " + self.id
        if hardware != None:
            self.constraints = And(self.constraints, self.hardware_id == hardware.index)

    def set_hardware(self, hardware):
        self.constraints = And(self.constraints, self.hardware_id == hardware.index)

    def bind_hardware(self, hardware):
        return hardware.get_constraints(self.configuration)

    def set_constraints(self):
        self.constrained_slots = {}
        for slot_name in CONSTRAINED_SLOTS[self.device_type]:
            self.constrained_slots[slot_name] = {}
            entries = []
            for universe_elem in CONSTRAINED_SLOTS[self.device_type][slot_name].universe:
                entries += list(universe_elem)
            for entry in entries:
                self.constrained_slots[slot_name][entry] = Real(self.id + "_" + slot_name + "_" + entry)
                VAR_DESCRIPTIONS[self.id + "_" + slot_name + "_" + entry] = "Constrained slot " + slot_name + " for " + self.id + " with id " + entry

        self.constraints = And(self.constraints,
            Or(*[self.hardware_id == x for x in range(len(HARDWARES[self.device_type]))]),
            And(*[Implies(self.hardware_id == RealVal(x), self.bind_hardware(HARDWARES[self.device_type][x])) for x in range(len(HARDWARES[self.device_type]))]),

            And(*[Sum([self.constrained_slots[slot_name][id] for id in self.constrained_slots[slot_name]]) <= self.configuration[slot_name] for slot_name in self.constrained_slots]),
            And(*[And(*[self.constrained_slots[slot_name][id] >= 0 for id in self.constrained_slots[slot_name]]) for slot_name in self.constrained_slots])
        )
    
    def set_device_property(self, key, value):
        if key not in self.device_properties:
            raise KeyError("Property not part of this topology")
        self.device_properties[key] = value

    def get_configuration(self, key, default_value):
        if key not in self.configuration.keys():
            return default_value
        return self.configuration[key]


class WorkloadProperties:
    def __init__(self, id):
        self.id = id
        WORKLOAD_PROPERTIES[id] = Bool(self.id)
        VAR_DESCRIPTIONS[self.id] = f"{self.id} is a property of the workload"


class Objective:
    def __init__(self, id):
        if id in OBJECTIVES:
            raise KeyError("Objective with", id, "already exists.")
        self.id = id
        OBJECTIVES[id] = Bool(self.id)
        VAR_DESCRIPTIONS[self.id] = f"{self.id} is an objective of the workload"


class Workload:
    def __init__(self, id, topology, properties, objectives, compute_load = 0, network_load = 0):
        self.id = id

        WORKLOADS[id] = self
        self.topology = topology
        topology.add_workload(self)

        self.support_modification = True
        self.performance_constraints = BoolVal(True)
        self.properties = properties
        self.objectives = objectives
        self.objective_weights = {}

        for objective_id in OBJECTIVES:
            self.objective_weights[objective_id] = 1

        self.compute_load = compute_load
        self.network_load = network_load

        self.solutions = {}
        self.roles_to_exempt = []
        self.solution_configs = {}
        self.alloted_solution_rewards = {}
        self.expected_solution_rewards = {}
        for objective_id in OBJECTIVES:
            if objective_id in map(lambda x: x.id, objectives):
                ALL_OBJECTIVES.append(OBJECTIVES[objective_id])
        for workload_property in WORKLOAD_PROPERTIES:
            if workload_property in map(lambda x: x.id, properties):
                ALL_PROPERTIES.append(WORKLOAD_PROPERTIES[workload_property])
                # SOLVER.assert_and_track(WORKLOAD_PROPERTIES[workload_property] == BoolVal(True), f"{workload_property} is a workload property")
                # TRACKED_CONSTRAINTS[f"{workload_property} is a workload property"] = WORKLOAD_PROPERTIES[workload_property] == BoolVal(True)

                # SOLVER.assert_and_track(WORKLOAD_PROPERTIES[workload_property] == BoolVal(False), f"{workload_property} is not a workload property")
                # TRACKED_CONSTRAINTS[f"{workload_property} is not a workload property"] = WORKLOAD_PROPERTIES[workload_property] == BoolVal(False)
        for solution_id in SYSTEMS:
            # print("Adding solution", solution_id, "to workload", id)
            self.solutions[solution_id] = Bool(id + "_" + solution_id)
            VAR_DESCRIPTIONS[id + "_" + solution_id] = "Solution " + solution_id + " for workload " + id
            self.solution_configs[solution_id] = {}
            for config in SYSTEMS[solution_id].configs:
                self.solution_configs[solution_id][config] = Bool(id + "_" + solution_id + "_" + config)
                VAR_DESCRIPTIONS[id + "_" + solution_id + "_" + config] = "Config " + config + " for solution " + solution_id + " in workload " + id
            self.alloted_solution_rewards[solution_id] = {}
            self.expected_solution_rewards[solution_id] = {}
            for objective_id in OBJECTIVES:
                self.alloted_solution_rewards[solution_id][objective_id] = Real(id + "_" + solution_id + "_" + objective_id + "_alloted_reward")
                VAR_DESCRIPTIONS[id + "_" + solution_id + "_" + objective_id + "_alloted_reward"] = "Alloted reward for " + solution_id + " for objective " + objective_id + " in workload " + id
                self.expected_solution_rewards[solution_id][objective_id] = Real(id + "_" + solution_id + "_" + objective_id + "_expected_reward")
                VAR_DESCRIPTIONS[id + "_" + solution_id + "_" + objective_id + "_expected_reward"] = "Expected reward for " + solution_id + " for objective " + objective_id + " in workload " + id
        
        self.alloted_role_rewards = {}
        for role_id in ROLES:
            self.alloted_role_rewards[role_id] = {}
            for objective_id in OBJECTIVES:
                self.alloted_role_rewards[role_id][objective_id] = Real(id + "_" + role_id + "_" + objective_id + "_alloted_reward_roles")
                VAR_DESCRIPTIONS[id + "_" + role_id + "_" + objective_id + "_alloted_reward_roles"] = "Alloted reward for " + role_id + " for objective " + objective_id + " in workload " + id

    def enable_solution(self, solution_id):
        SOLVER.add(self.solutions[solution_id])

    def set_objective_weightage(self, objective, weight):
        self.objective_weights[objective.id] = weight
    
    def set_performance_bound(self, role, objective, atleast = None, atleast_value = -1):
        if not atleast == None:
            self.performance_constraints = And(self.performance_constraints, self.alloted_role_rewards[role.id][objective.id] >= self.expected_solution_rewards[atleast.id][objective.id])
        elif not atleast_value == -1:
            self.performance_constraints = And(self.performance_constraints, self.alloted_role_rewards[role.id][objective.id] >= Real(atleast_value))
        else:
            raise ArgumentError("Either of atleast or atleast_value should be provided")

    def set_constraints(self):
        impacted_computes = self.topology.get_children(device_type = DEVICE_TYPE.COMPUTE)
        impacted_links = self.topology.get_children(device_type = DEVICE_TYPE.LINK)
        impacted_routers = self.topology.get_children(device_type = DEVICE_TYPE.ROUTER)

        # self.property_constraints = And(*[WORKLOAD_PROPERTIES[_property.id] == True for _property in self.properties])
        # self.property_constraints = And(self.property_constraints, *[WORKLOAD_PROPERTIES[_propertyId] == False for _propertyId in WORKLOAD_PROPERTIES if _propertyId not in map(lambda x: x.id, self.properties)])

        self.constraints = And(
            self.performance_constraints,
            And(*[compute.constrained_slots["cores"][self.id] == self.compute_load for compute in impacted_computes]),
            And(*[link.constrained_slots["bandwidth"][self.id] == self.network_load for link in impacted_links]),

            And(get_ordering_constraints(self)),

            And(*[self.solutions[id] == BoolVal(False) for id in SYSTEMS if SYSTEMS[id].role in self.roles_to_exempt]),

            # Bound alloted and expected rewards
            And(*[self.alloted_solution_rewards[solution_id][objective_id] >= 0 for solution_id in SYSTEMS for objective_id in OBJECTIVES]),
            And(*[self.expected_solution_rewards[solution_id][objective_id] >= 0 for solution_id in SYSTEMS for objective_id in OBJECTIVES]),
            And(*[self.alloted_solution_rewards[solution_id][objective_id] <= 100 for solution_id in SYSTEMS for objective_id in OBJECTIVES]),
            And(*[self.expected_solution_rewards[solution_id][objective_id] <= 100 for solution_id in SYSTEMS for objective_id in OBJECTIVES]),

            # If solution X is enabled, we should also get it's reward
            And(*[Implies(self.solutions[id], And(*[self.alloted_solution_rewards[id][objective_id] == self.expected_solution_rewards[id][objective_id] for objective_id in OBJECTIVES])
            ) for id in self.solutions]),

            And(*[self.alloted_role_rewards[role_id][objective_id] == Sum(*[self.alloted_solution_rewards[solution_id][objective_id] for solution_id in SYSTEMS if SYSTEMS[solution_id].role == ROLES[role_id]]) for role_id in ROLES for objective_id in OBJECTIVES]),

            # If solution X is enabled, no other solution with the same role can be enabled
            And(*[Implies(self.solutions[id], And(*[Not(self.solutions[id_2]) for id_2 in self.solutions if SYSTEMS[id_2].role == SYSTEMS[id].role and not id == id_2 and SYSTEMS[id].role.exclusive])) for id in self.solutions]),

            # If solution X is not enabled, we don't get any reward for it
            And(*[Implies(Not(self.solutions[id]), And(*[self.alloted_solution_rewards[id][objective_id] == 0 for objective_id in OBJECTIVES])
                          ) for id in self.solutions]),

            # If solution X is enabled, then the constraints to enable that solution should be satisfied
            And(*[Implies(self.solutions[id], SYSTEMS[id].apply(self)) for id in self.solutions]),

            # Atleast one solution should be enabled
            # TODO: This might not be needed!
            Or(*[self.solutions[id] for id in self.solutions]),

            # If the solution is not deployed, all the configurations for that solution should be off
            And(*[Implies(Not(self.solutions[id]), And(*[Not(self.solution_configs[id][config]) for config in SYSTEMS[id].configs])) for id in self.solutions if not SYSTEMS[id].configs == []]),
            
            # If ths solution is deployed, the atleast one config should be enabled
            And(*[Implies(self.solutions[id], Or(*[self.solution_configs[id][config] for config in SYSTEMS[id].configs])) for id in self.solutions if not SYSTEMS[id].configs == []]),

            # If ths solution is deployed, the exactly one config should be enabled
            And(*[Implies(self.solution_configs[id][config], And(*[Not(self.solution_configs[id][config2]) for config2 in SYSTEMS[id].configs if not config2 == config])) for id in self.solution_configs for config in self.solution_configs[id]])
        )
        if high_priority in self.objectives:
            self.constraints = And(
                self.constraints,
                And(*[router.constrained_slots["QoS"][self.id] == 1 for router in impacted_routers]),
            )


class Role:
    def __init__(self, id, problem_condition = lambda workload: BoolVal(True), message = None):
        self.id = id
        ROLES[id] = self
        self.problem_condition = problem_condition
        self.message = message
        self.solvers = []
        # self.needs_solving = Bool(id + "_needs_solving")
        VAR_DESCRIPTIONS[id + "_needs_solving"] = "Role " + self.id + " needs solving"
        self.needs_solving = True
        self.to_warn = True
        self.exclusive = True
        self.exclusive_var = Bool(id + "_exclusive")
        VAR_DESCRIPTIONS[id + "_exclusive"] = "Role " + self.id + " is exclusive"
        self.is_solved = Bool(id + "_is_solved")
        VAR_DESCRIPTIONS[id + "_is_solved"] = "Role " + self.id + " is solved"
    
    def disable_solving(self):
        self.needs_solving = False

    def disable_warning(self):
        self.to_warn = False

    def set_constraints(self):
        if self.message == None:
            self.message = "No system deployed to solve " + self.id + "."
        # self.message = self.message + " The problem can be fixed using one of these systems: " + ", ".join(self.solvers)
        self.constraints = And(
                               # self.needs_solving,

                               self.exclusive_var == self.exclusive,

                               Implies(BoolVal(self.needs_solving), self.is_solved),

                               # For all workloads, either the problem is solved, or atleast one of the solutions is enabled, implies that the role 'is solved'
                               Implies(And(*[Or(Not(self.problem_condition(WORKLOADS[workload_id])), Or(*[WORKLOADS[workload_id].solutions[solution] for solution in self.solvers])) for workload_id in WORKLOADS if self not in WORKLOADS[workload_id].roles_to_exempt]), self.is_solved),

                               # For all workloads, !(Either the problem is solved, or a system is deployed), implies that the role is not solved
                               Implies(Not(And(*[Or(Not(self.problem_condition(WORKLOADS[workload_id])), Or(*[WORKLOADS[workload_id].solutions[solution] for solution in self.solvers])) for workload_id in WORKLOADS if self not in WORKLOADS[workload_id].roles_to_exempt])), Not(self.is_solved)),

                               # For all workloads, if the problem is already solved, then no solutions should be enabled for it
                               And(*[Implies(Not(self.problem_condition(WORKLOADS[workload_id])), And(*[Not(WORKLOADS[workload_id].solutions[solution]) for solution in self.solvers])) for workload_id in WORKLOADS])
                            )

    def add_solver(self, solution):
        self.solvers.append(solution.id)


class System:
    def __init__(self, id, role, apply, objectives = [], configs = [], message = None):
        self.id = id
        SYSTEMS[self.id] = self
        self.role = role
        self.objectives = objectives
        # self.apply = lambda workload: And(apply(workload), has_intersection(self, workload, workload.objectives, self.objectives))
        self.apply = lambda workload: And(apply(workload))
        self.message = message
        self.warnings = []
        role.add_solver(self)
        self.configs = configs
    
    def add_warning(self, id, condition, message):
        self.warnings.append([id, condition, message])

class SuggestedOrdering:
    def __init__(self, id, objective, system, better_than = None, same_as = None, exact_value = -1, condition = lambda workload: BoolVal(True)):
        if better_than == None and same_as == None and exact_value == -1:
            raise ArgumentError("Either of better_than, same_as, or exact value must be specified")
        SUGGESTED_ORDERINGS.append(self)
        self.id = id
        self.system = system
        self.better_than = better_than
        self.same_as = same_as
        self.exact_value = exact_value
        self.condition = condition
        self.objective = objective
        self.enable = True

class Ordering:
    def __init__(self, objective, system, better_than = None, same_as = None, exact_value = -1, condition = lambda workload: BoolVal(True)):
        if better_than == None and same_as == None and exact_value == -1:
            raise ArgumentError("Either of better_than, same_as, or exact value must be specified")
        ORDERINGS.append(self)
        self.system = system
        self.better_than = better_than
        self.same_as = same_as
        self.exact_value = exact_value
        self.condition = condition
        self.objective = objective
        if objective not in system.objectives:
            system.objectives.append(objective)
        if not better_than == None and objective not in better_than.objectives:
            better_than.objectives.append(objective)
        if not same_as == None and objective not in same_as.objectives:
            same_as.objectives.append(objective)

def get_ordering_constraints(workload):
    constraints = []
    for ordering in ORDERINGS:
        if not ordering.better_than == None:
            constraints.append(Implies(ordering.condition(workload), workload.expected_solution_rewards[ordering.system.id][ordering.objective.id] >= workload.expected_solution_rewards[ordering.better_than.id][ordering.objective.id] + 1))
        elif not ordering.same_as == None:
            constraints.append(Implies(ordering.condition(workload), workload.expected_solution_rewards[ordering.system.id][ordering.objective.id] == workload.expected_solution_rewards[ordering.same_as.id][ordering.objective.id]))
        elif not ordering.exact_value == -1:
            constraints.append(Implies(ordering.condition(workload), workload.expected_solution_rewards[ordering.system.id][ordering.objective.id] == RealVal(ordering.exact_value)))

    for system_id in SYSTEMS:
        for objective_id in OBJECTIVES:
            if objective_id not in map(lambda x: x.id, SYSTEMS[system_id].objectives):
                constraints.append(workload.expected_solution_rewards[system_id][objective_id] == 0)
    return And(*[constraints])


class Optimize:
    def __init__(self, workload, objective, priority):
        OPTIMIZERS[objective.id] = self
        self.workload = workload
        self.objective = objective
        self.priority = priority

# Helper functions after all policies, devices, and applications have been setup.
def add_topology_constraints(solver):
    # Access Total cost, performance as local variables
    global TOTAL_COST, PERFORMANCE

    # update_system_graph(HARDWARES, DEVICE_TYPE, SYSTEM_GRAPH)

    for ordering in SUGGESTED_ORDERINGS:
        if ordering.enable:
            Ordering(ordering.objective, ordering.system, ordering.better_than, ordering.same_as, ordering.exact_value, ordering.condition)

    for device_id in DEVICES:
        DEVICES[device_id].set_constraints()
        TRACKED_CONSTRAINTS[device_id] = DEVICES[device_id].constraints
        solver.assert_and_track(DEVICES[device_id].constraints, device_id)

    for workload_id in WORKLOADS:
        WORKLOADS[workload_id].set_constraints()
        TRACKED_CONSTRAINTS[workload_id] = WORKLOADS[workload_id].constraints
        solver.assert_and_track(WORKLOADS[workload_id].constraints, workload_id)


        for system_id in SYSTEMS:
            # Warnings ignored for explainability
            for warning in SYSTEMS[system_id].warnings:
                solver.add(Implies(And(WORKLOADS[workload_id].solutions[system_id], warning[1]), Bool(system_id + "_" + warning[0])))

    for role_id in ROLES:
        ROLES[role_id].set_constraints()
        TRACKED_CONSTRAINTS[role_id] = ROLES[role_id].constraints
        solver.assert_and_track(ROLES[role_id].constraints, role_id)

    for workload_property in ALL_PROPERTIES:
            SOLVER.assert_and_track(workload_property == BoolVal(True), f"{str(workload_property)} is a workload property")
            TRACKED_CONSTRAINTS[f"{str(workload_property)} is a workload property"] = workload_property == BoolVal(True)

    for workload_property in WORKLOAD_PROPERTIES:
        if WORKLOAD_PROPERTIES[workload_property] not in ALL_PROPERTIES:
                SOLVER.assert_and_track(WORKLOAD_PROPERTIES[workload_property] == BoolVal(False), f"{workload_property} is not a workload property")
                TRACKED_CONSTRAINTS[f"{workload_property} is not a workload property"] = WORKLOAD_PROPERTIES[workload_property] == BoolVal(False)

    
    OPTIMIZERS_SORTED = sorted(OPTIMIZERS.values(), key=lambda x: x.priority)
    for optimizer in OPTIMIZERS_SORTED:
        if type(optimizer.workload) == str:
            if optimizer.workload == "COST":
                print("Trying to minimize cost")
                SOLVER.minimize(TOTAL_COST)
            if optimizer.workload == "FREE_CORES":
                print("Trying to minimize free cores")
                SOLVER.minimize(Sum([DEVICES[device_id].constrained_slots["cores"][x] for device_id in DEVICES if DEVICES[device_id].device_type == DEVICE_TYPE.COMPUTE for x in DEVICES[device_id].constrained_slots["cores"]]))
            if optimizer.workload == "QUEUES":
                print("Trying to minimize queues")
                SOLVER.minimize(Sum([DEVICES[device_id].configuration["QoS"] for device_id in DEVICES if DEVICES[device_id].device_type == DEVICE_TYPE.ROUTER]))
            continue

        reward = Real("Optimizer_reward_" + optimizer.objective.id + "_" + optimizer.workload.id)
        VAR_DESCRIPTIONS["Optimizer_reward_" + optimizer.objective.id + "_" + optimizer.workload.id] = "Optimizer reward for objective " + optimizer.objective.id + "for workload" + optimizer.workload.id
        solver.add(reward == Sum([optimizer.workload.alloted_solution_rewards[solution_id][optimizer.objective.id] for solution_id in SYSTEMS]))
        solver.maximize(reward)

    solver.add(TOTAL_COST == Sum([DEVICES[device_id].configuration["cost"] for device_id in DEVICES]))


def break_and(and_expr):
    assert is_and(and_expr)
    return and_expr.children()

# Break down AND constraints to simplify clauses and give better explainations
def track_atomic(hl_expr, solver, recursive = False, assertion_name = None):
    global counter
    if is_and(hl_expr):
        for arg in hl_expr.children():
            track_atomic(arg, solver, recursive = True)
    else:
        if recursive:
            track_var = f"track_{counter}"
            counter = counter + 1
            TRACKED_CONSTRAINTS[track_var] = hl_expr
            solver.assert_and_track(hl_expr, track_var)
        else:
            solver.assert_and_track(hl_expr, assertion_name)

# Break down AND and IMPLIES constraints to simplify clauses and give better explainations
def track_atomic_fine(hl_expr, solver, recursive = False, assertion_name = None):
    global counter
    if is_and(hl_expr):
        for arg in hl_expr.children():
            track_atomic_fine(arg, solver, recursive = True)
    elif is_implies(hl_expr) and is_and(hl_expr.arg(1)):
        constraint_list = break_and(hl_expr.arg(1))
        for constraint in constraint_list:
            track_var = f"track_{counter}"
            counter = counter + 1
            TRACKED_CONSTRAINTS[track_var] = Implies(hl_expr.arg(0), constraint)
            solver.assert_and_track(Implies(hl_expr.arg(0), constraint), track_var)
    else:
        if recursive:
            track_var = f"track_{counter}"
            counter = counter + 1
            TRACKED_CONSTRAINTS[track_var] = hl_expr
            solver.assert_and_track(hl_expr, track_var)
        else:
            solver.assert_and_track(hl_expr, assertion_name)

# Print better explanations from unsat core
def print_atomic(hl_expr):
    str_expr = str(hl_expr)
    re_str_expr = str_expr.replace("(", " ( ")
    re_str_expr = re_str_expr.replace(")", " ) ")
    re_str_expr = re_str_expr.replace(",", " , ")
    re_str_expr = re_str_expr.replace("{", " { ")
    re_str_expr = re_str_expr.replace("}", " } ")
    re_str_expr = re_str_expr.replace("[", " [ ")
    re_str_expr = re_str_expr.replace("]", " ] ")
    lst_expr = re_str_expr.split(" ")
    for i in range(len(lst_expr)):
        try:
            update_str = VAR_DESCRIPTIONS[lst_expr[i]]
            lst_expr[i] = update_str
        except KeyError:
            pass
    print(" ".join(lst_expr))

# Get the top system according to orderings
def get_order(workload, curr_system, property_name):
    curr_system_expected_solutions = WORKLOADS[workload].expected_solution_rewards[curr_system][property_name]
    curr_system_expected_solutions_val = float(ASSIGNMENT_DICT[str(curr_system_expected_solutions)].numerator_as_long() / ASSIGNMENT_DICT[str(curr_system_expected_solutions)].denominator_as_long())
    priority_systems = []
    for system in SYSTEMS.keys():
        if SYSTEMS[system].role.id == SYSTEMS[curr_system].role.id:
            system_expected_solutions = WORKLOADS[workload].expected_solution_rewards[str(system)][property_name]
            system_expected_solutions_val = float(ASSIGNMENT_DICT[str(system_expected_solutions)].numerator_as_long() / ASSIGNMENT_DICT[str(system_expected_solutions)].denominator_as_long())
            if system_expected_solutions_val > curr_system_expected_solutions_val:
                priority_systems.append([system, system_expected_solutions_val])
    priority_systems.sort(key=lambda x: x[1], reverse=True)
    def get_system(system_expected_reward):
        assert len(system_expected_reward) == 2
        return system_expected_reward[0]
    priority_systems = list(map(get_system, priority_systems))
    return priority_systems


def evaluate(solver=SOLVER, debug = False, explain = False, recursive = False):
    global SOLVER_UNSAT

    start = time.time()
    if recursive == False:
        print(HARDWARE_ID_MAPPING)
    if str(solver.check()) == "sat":
        allocations = solver.model()
        print("Time taken by z3 to solve", time.time() - start)

        assignment_lst = []
        for i in allocations.decls():
            if (type(allocations[i]) == BoolRef and allocations[i] == True) or (type(allocations[i]) == RatNumRef):
                assignment_lst.append((i.name(), allocations[i]))

        assignment_lst.sort(key=lambda x: x[0])
        print("\n** Assignments **")
        for assignment in assignment_lst:
            ASSIGNMENT_DICT[assignment[0]] = assignment[1]

        hardware_assignments = []
        if debug:
            print("\n** Hardware assignments **")
            for elem in allocations.decls():
                name = elem.name()
                if name.endswith(HARDWARE_VARIABLES_SUFFIX):
                    value = allocations[elem].as_long()
                    hardware_assignments.append(f"{name} == {value}")
                    hardware_type = name.rstrip(HARDWARE_VARIABLES_SUFFIX).split(".")[-1]
                    print(name.rstrip(HARDWARE_VARIABLES_SUFFIX), "=", HARDWARES[DEVICE_TYPE[hardware_type]][value].id)

        print("\n** Systems deployed **")
        for workload_id in WORKLOADS:
            print(workload_id, "-")
            index = 1
            for system_id in SYSTEMS:
                key = workload_id + "_" + system_id
                for elem in allocations.decls():
                    name = elem.name()
                    value = allocations[elem]
                    if key == name and value == True:
                        print(str(index) + ". " + SYSTEMS[system_id].role.id + " role: " + system_id)
                        index += 1
                        if not SYSTEMS[system_id].message == None:
                            if WARNINGS:
                                print("Warning:", SYSTEMS[system_id].message)
            print("")

        warning_index = 0
        for system_id in SYSTEMS:
            for warning in SYSTEMS[system_id].warnings:
                key = system_id + "_" + warning[0]
                for elem in allocations.decls():
                    name = elem.name()
                    value = allocations[elem]
                    if key == name:
                        if warning_index == 0:
                            print("\n** System warnings **")
                        warning_index += 1
                        print(str(warning_index) + ". " + warning[2])

        role_index = 0
        for role_id in ROLES:
            key = role_id + "_is_solved"
            for elem in allocations.decls():
                name = elem.name()
                value = allocations[elem]
                if key == name:
                    if value == False and ROLES[role_id].to_warn and ROLES[role_id].needs_solving:
                        if role_index == 0:
                            print("\n** Problems **")
                        role_index += 1
                        print(str(role_index) + ". " + ROLES[role_id].message)

        print("\n** Other values **")
        for elem in allocations.decls():
            name = elem.name()
            if name in ["Total cost"]:
                value = allocations[elem].as_long()
                print(name, "=", value)
            # CHANGE BACK IF REQUIRED!
            if False:
                if "reward" in name:
                    print(name)
                    value = allocations[elem].as_long()
                    print(name, "=", value)
        
    else: # Else case where no solutions are found and explainability workflow needs to be triggered
        print("No feasible solution found")

        if bool(explain) == True:
            if "Fix cost" in map(lambda x: str(x), solver.unsat_core()):
                print("CANNOT FIND CONFIGURATION WITH LOWER COST!!")
                return
            
            # Break down constraints and try again
            for assertion in solver.unsat_core():
                track_atomic_fine(TRACKED_CONSTRAINTS[str(assertion)], solver=SOLVER_UNSAT, assertion_name=str(assertion))

            SOLVER_UNSAT.check()

            # Break down constraints (that are already broken down!) and try again
            next_unsat_core_fine = SOLVER_UNSAT.unsat_core()
            # for assertion in next_unsat_core:
            #     track_atomic_fine(TRACKED_CONSTRAINTS[str(assertion)], solver=SOLVER_UNSAT_FINE, assertion_name=str(assertion))

            # SOLVER_UNSAT_FINE.check()
            # next_unsat_core_fine = SOLVER_UNSAT_FINE.unsat_core()
            print("Unsat core:", next_unsat_core_fine)
            print("")
            print("CHOICES")
            print("")
            for assertion in next_unsat_core_fine:
                if ("enable" in str(assertion) and TRACKED_CONSTRAINTS[str(assertion)].decl().kind() == Z3_OP_EQ):
                    print_atomic(TRACKED_CONSTRAINTS[str(assertion)])
                    print("-------")
                    
            print("@@@@@@@@@@@@@@@@@@@@@@@@@")

            print("")
            print("CONSTRAINTS")
            print("")
            for assertion in next_unsat_core_fine:
                if (TRACKED_CONSTRAINTS[str(assertion)].decl().kind() != Z3_OP_EQ):
                    print_atomic(TRACKED_CONSTRAINTS[str(assertion)])
                    print("-------")
            
# Entry function to track and assert constraints and fix choices before reevaluation of the constraints for explainability
def explain(workload, order_role, order_objective, fix_hardware=None, fix_roles=None, priority_number=0, solver=SOLVER, solver_unsat=SOLVER_UNSAT):

    if len(ASSIGNMENT_DICT) == 0:
        evaluate(solver, debug = True, explain = True, recursive  = True)
        return

    # Fix hardware choices
    if fix_hardware is not None:
        if fix_hardware == "all":
            for k in DEVICES.keys():
                val = ASSIGNMENT_DICT[k + HARDWARE_VARIABLES_SUFFIX]
                solver.assert_and_track((DEVICES[k].hardware_id == RealVal(val)), f"h_{k}")
                TRACKED_CONSTRAINTS[f"h_{k}"] = (DEVICES[k].hardware_id == RealVal(val))
        else:
            for k in fix_hardware:
                val = ASSIGNMENT_DICT[k + HARDWARE_VARIABLES_SUFFIX]
                solver.assert_and_track((DEVICES[k].hardware_id == RealVal(val)), f"h_{k}")
                TRACKED_CONSTRAINTS[f"h_{k}"] = (DEVICES[k].hardware_id == RealVal(val))

    # Fix COST
    solver.assert_and_track((TOTAL_COST <= RealVal(int(str(ASSIGNMENT_DICT["Total cost"])))), "Fix cost")
    TRACKED_CONSTRAINTS["Fix cost"] = (TOTAL_COST <= RealVal(int(str(ASSIGNMENT_DICT["Total cost"]))))

    # Fix system choices
    curr_system = None
    for k in (WORKLOADS[workload].solutions):
        if str(WORKLOADS[workload].solutions[k]) in ASSIGNMENT_DICT.keys() and SYSTEMS[str(k)].role.id != order_role and (fix_roles == None or (SYSTEMS[str(k)].role.id in fix_roles)):
            solver.assert_and_track(WORKLOADS[workload].solutions[str(k)] == BoolVal(True), f"{k}_keep_enabled")
            TRACKED_CONSTRAINTS[f"{k}_keep_enabled"] = (WORKLOADS[workload].solutions[str(k)] == BoolVal(True))
        if str(WORKLOADS[workload].solutions[k]) in ASSIGNMENT_DICT.keys() and SYSTEMS[str(k)].role.id == order_role:
            curr_system = k

    # Force choosing higher priority systems that isn't chosen yet
    high_priority_systems = get_order(workload, curr_system, order_objective)
    print("High priority systems for", workload, "than", curr_system, ":", high_priority_systems)
    if len(high_priority_systems) == 0:
        return
    solver.assert_and_track(WORKLOADS[workload].solutions[str(high_priority_systems[priority_number])] == True, f"{str(high_priority_systems[priority_number])}_enable")
    TRACKED_CONSTRAINTS[f"{str(high_priority_systems[priority_number])}_enable"] = (WORKLOADS[workload].solutions[str(high_priority_systems[priority_number])] == True)
    evaluate(solver, debug = True, explain = True, recursive  = True)

# Helper functions to create rack, pod with a given template
def create_rack(id, num_cpus):
    id = id + "IN-RACK"
    router = Device(id, DEVICE_TYPE.ROUTER)
    computes = [Device(get_id(id, index), DEVICE_TYPE.COMPUTE) for index in range(num_cpus)]
    links = [Device(get_id(id, index), DEVICE_TYPE.LINK) for index in range(num_cpus)]

    for index, link in enumerate(links):
        link.set_device_property("nodeA", router)
        link.set_device_property("nodeB", computes[index])
        computes[index].set_device_property("links", [link])

    router.set_device_property("links", links)

    rack = DeviceGroup(id, DEVICEGROUP_TYPE.RACK)
    rack.add_children([router] + computes + links)
    rack.set_property("TOR", router)
    rack.set_property("TOP_SWITCH", router)
    return rack

def create_rack_storage(id, num_storage):
    id = id + "IN-RACK"
    router = Device(id, DEVICE_TYPE.ROUTER)
    storage = [Device(get_id(id, index), DEVICE_TYPE.STORAGE) for index in range(num_storage)]
    links = [Device(get_id(id, index), DEVICE_TYPE.LINK) for index in range(num_storage)]

    for index, link in enumerate(links):
        link.set_device_property("nodeA", router)
        link.set_device_property("nodeB", storage[index])
        storage[index].set_device_property("links", [link])

    router.set_device_property("links", links)
    rack = DeviceGroup(id, DEVICEGROUP_TYPE.RACK)
    rack.add_children([router] + storage + links)
    rack.set_property("TOR", router)
    rack.set_property("TOP_SWITCH", router)
    return rack



def create_pod(id, num_racks, num_routers, num_cpus):
    id = id + "IN-POD"
    racks = [create_rack(get_id(id, index), num_cpus) for index in range(num_racks)]
    routers = [Device(get_id(id, index), DEVICE_TYPE.ROUTER) for index in range(num_routers)]
    links = []

    for router_index in range(num_routers):
        for rack_index in range(num_racks):
            link = Device(get_id(id, router_index, rack_index), DEVICE_TYPE.LINK)
            link.set_device_property("nodeA", routers[router_index])
            link.set_device_property("nodeB", racks[rack_index].devicegroup_properties["TOR"])
            racks[rack_index].devicegroup_properties["TOR"].set_device_property("links", [link])
            links.append(link)

    for router in routers:
        router.set_device_property("links", links)

    pod = DeviceGroup(id, DEVICEGROUP_TYPE.POD)
    pod.add_children(racks + routers + links)
    pod.set_property("POD_ROUTERS", routers)
    pod.set_property("TOP_SWITCH", routers[0])

    return pod


def create_microservice_pod(id, num_racks, num_routers=None, num_cpus=None, num_storage=None):
    id = id + "IN-POD"
    if num_storage != None:
        storage_racks = [create_rack_storage(get_id(id, index), num_storage) for index in range(1)]
    else:
        storage_racks = []
    if num_cpus != None:
        compute_racks = [create_rack(get_id(id, index), num_cpus) for index in range(1, max(1, num_racks) + 1)]
    else:
        compute_racks = []
    if num_routers != None:
        routers = [Device(get_id(id, index), DEVICE_TYPE.ROUTER) for index in range(num_routers)]
    else:
        routers = []
    links = []

    for router_index in range(len(routers)):
        for rack_index in range(len(compute_racks)):
            link = Device(get_id(id, router_index, rack_index), DEVICE_TYPE.LINK)
            link.set_device_property("nodeA", routers[router_index])
            link.set_device_property("nodeB", compute_racks[rack_index].devicegroup_properties["TOR"])
            compute_racks[rack_index].devicegroup_properties["TOR"].set_device_property("links", [link])
            links.append(link)

        for rack_index in range(len(storage_racks)):
            link = Device(get_id(id, router_index, rack_index, "storage"), DEVICE_TYPE.LINK)
            link.set_device_property("nodeA", routers[router_index])
            link.set_device_property("nodeB", storage_racks[rack_index].devicegroup_properties["TOR"])
            storage_racks[rack_index].devicegroup_properties["TOR"].set_device_property("links", [link])
            links.append(link)

    for router in routers:
        router.set_device_property("links", links)

    pod = DeviceGroup(id, DEVICEGROUP_TYPE.POD)
    pod.add_children(compute_racks + storage_racks + routers + links)
    pod.set_property("POD_ROUTERS", routers)
    pod.set_property("TOP_SWITCH", routers[0])

    return pod


LinkProperties = DeviceProperties(DEVICE_TYPE.LINK)
LinkProperties.add_property("nodeA")
LinkProperties.add_property("nodeB")

RouterProperties = DeviceProperties(DEVICE_TYPE.ROUTER)
RouterProperties.add_property("links", [])

ComputeProperties = DeviceProperties(DEVICE_TYPE.COMPUTE)
ComputeProperties.add_property("links", [])

StorageProperties = DeviceProperties(DEVICE_TYPE.STORAGE)
StorageProperties.add_property("links", [])

RackProperties = DeviceGroupProperties(DEVICEGROUP_TYPE.RACK)
RackProperties.add_property("TOR", None)
RackProperties.add_property("TOP_SWITCH", None)

PodProperties = DeviceGroupProperties(DEVICEGROUP_TYPE.POD)
PodProperties.add_property("POD_ROUTERS", [])
PodProperties.add_property("TOP_SWITCH", None)
PodProperties.add_property("CyclicBufferDep", False)

DCProperties = DeviceGroupProperties(DEVICEGROUP_TYPE.DC)
DCProperties.add_property("POP", None)
DCProperties.add_property("Reordering", 0)

LinkConfig = HardwareConfiguration(DEVICE_TYPE.LINK)
LinkConfig.add_configuration("cost", Real, 0)
LinkConfig.add_configuration("fibre_type", Real, 0)

RouterConfig = HardwareConfiguration(DEVICE_TYPE.ROUTER)
RouterConfig.add_configuration("cost", Real, 0)
RouterConfig.add_configuration("INT", Bool, False)
RouterConfig.add_configuration("ECN", Bool, False)
RouterConfig.add_configuration("P4", Bool, False)
RouterConfig.add_configuration("throughput_Gbps", Real, 0)


ComputeConfig = HardwareConfiguration(DEVICE_TYPE.COMPUTE)
ComputeConfig.add_configuration("cost", Real, 0)
ComputeConfig.add_configuration("NIC_TIMESTAMPS", Bool, False)
ComputeConfig.add_configuration("NIC_Reorder_Buffer", Real, 0)
ComputeConfig.add_configuration("NIC_loss_recovery_go_back_n", Bool, False)
ComputeConfig.add_configuration("NIC_loss_recovery_fancy", Bool, False)
ComputeConfig.add_configuration("FPGA", Bool, False)
ComputeConfig.add_configuration("SMART_NIC", Bool, False)
ComputeConfig.add_configuration("RDMA", Bool, False)
ComputeConfig.add_configuration("supports_wasm_runtime", Bool, False)
ComputeConfig.add_configuration("supports_wasi", Bool, False)
ComputeConfig.add_configuration("supports_namespaces", Bool, False)
ComputeConfig.add_configuration("supports_cgroups", Bool, False)
ComputeConfig.add_configuration("supports_cni", Bool, False)
ComputeConfig.add_configuration("supports_iptables", Bool, False)
ComputeConfig.add_configuration("supports_nftables", Bool, False)
ComputeConfig.add_configuration("supports_ebpf", Bool, False)
ComputeConfig.add_configuration("supports_overlayfs", Bool, False)
ComputeConfig.add_configuration("power_W", Real, 100000)
ComputeConfig.add_configuration("network_bandwidth_Gbps", Real, 0)
ComputeConfig.add_configuration("TPU", Bool, False)
ComputeConfig.add_configuration("GPU", Bool, False)
ComputeConfig.add_configuration("virtualization_support", String, "")
ComputeConfig.add_configuration("arch", String, "")


StorageConfig = HardwareConfiguration(DEVICE_TYPE.STORAGE)
StorageConfig.add_configuration("cost", Real, 0)
StorageConfig.add_configuration("IOPS", Real, 0)
StorageConfig.add_configuration("network_bandwidth_Gbps", Real, 0)
StorageConfig.add_configuration("file_descriptor_limit", Real, 0)
StorageConfig.add_configuration("power_W", Real, 1000000)


ConstrainedSlot("bandwidth", DEVICE_TYPE.LINK)
ConstrainedSlot("cores", DEVICE_TYPE.COMPUTE)
ConstrainedSlot("cores", DEVICE_TYPE.ROUTER)
ConstrainedSlot("cores", DEVICE_TYPE.STORAGE)
ConstrainedSlot("QoS", DEVICE_TYPE.ROUTER)
ConstrainedSlot("memory", DEVICE_TYPE.ROUTER)
ConstrainedSlot("P4-stages", DEVICE_TYPE.ROUTER)
ConstrainedSlot("memory_GB", DEVICE_TYPE.COMPUTE)
ConstrainedSlot("memory_GB", DEVICE_TYPE.STORAGE)
ConstrainedSlot("storage_GB", DEVICE_TYPE.STORAGE)
ConstrainedSlot("storage_GB", DEVICE_TYPE.COMPUTE)
ConstrainedSlot("GPU_memory_GB", DEVICE_TYPE.COMPUTE)
ConstrainedSlot("TPU_memory_GB", DEVICE_TYPE.COMPUTE)
ConstrainedSlot("FPGA-capacity", DEVICE_TYPE.COMPUTE)

# Roles
cca = Role("cca")
virtual_switch = Role("virtual_switch")
virtual_switch.to_warn = False
transport = Role("transport")
cpu_sched = Role("cpu_sched")
load_balancer = Role("load_balancer")
monitor = Role("Monitor")

def wan_dc_compeition_condition(workload):
    links = workload.topology.get_children(device_type = DEVICE_TYPE.LINK)
    for link in links:
        wan_exists, dc_exists = False, False
        for workload in link.workloads:
            if wan_flows in workload.properties:
                wan_exists = True
            if dc_flows in workload.properties:
                dc_exists = True
        
        if wan_exists and dc_exists:
            return Bool(True)

    return Bool(False)

def starvation_condition(workload):
    links = workload.topology.get_children(device_type = DEVICE_TYPE.LINK)
    for link in links:
        wan_exists, dc_exists = False, False
        for workload in link.workloads:
            if wan_flows in workload.properties:
                wan_exists = True
            if dc_flows in workload.properties:
                dc_exists = True
        
        if wan_exists and dc_exists:
            return Bool(True)
    
    return Bool(False)

def internet_condition(workload):
    if internet_flows in workload.properties:
        return Bool(True)
    
    return Bool(False)

# Objectives
latency=Objective("latency")
jitter = Objective("jitter")
throughput=Objective("throughput")
fairness = Objective("fairness")
load_balancing = Objective("load_balancing")
host_resource_isolation = Objective("host_resource_isolation")
address_space_isolation = Objective("address_space_isolation")
compute_efficiency = Objective("efficiency")
ease_of_deployment = Objective("ease_of_deployment")
application_modification = Objective("application_modification")
multi_tenancy = Objective("multi_tenancy")
security = Objective("security")
monitoring = Objective("monitoring")
loss_less = Objective("loss_less")
scavenger = Objective("scavenger")
fault_tolerance = Objective("fault_tolerance")
high_availability = Objective("high_availability")
cost_efficiency = Objective("cost_efficiency")
low_utilization = Objective("low_utilization")
high_priority = Objective("high_priority")


# Properties
short_flows=WorkloadProperties("short_flows")
long_flows = WorkloadProperties("long_flows")

wan_flows = WorkloadProperties("wan_flows")
dc_flows=WorkloadProperties("dc_flows")
internet_flows = WorkloadProperties("internet_flows")

high_priority = WorkloadProperties("high_priority")
regular_priority = WorkloadProperties("regular_priority")
low_priority = WorkloadProperties("low_priority")

incast=WorkloadProperties("incast")

ml_training = WorkloadProperties("MLTraining")
hpc = WorkloadProperties("HPC")
cdn = WorkloadProperties("CDN")
microservices = WorkloadProperties("Microservices")
bigdata = WorkloadProperties("BigData")
reorder_tolerant = WorkloadProperties("reorder_tolerant")
short_spans = WorkloadProperties("short_spans")
low_sampling = WorkloadProperties("low_sampling")
application_observability = WorkloadProperties("application_observability")
l7_load_balancing = WorkloadProperties("l7_load_balancing") 
external_resources = WorkloadProperties("external_resources")
syscall_latency_scaling = WorkloadProperties("syscall-latency_scaling")
heterogenous = WorkloadProperties("Heterogenous")
low_load = WorkloadProperties("Low Load")
medium_load = WorkloadProperties("Medium Load")
high_load = WorkloadProperties("High Load")
non_root = WorkloadProperties("Non-root")
go = WorkloadProperties("Go")
c_plus_plus = WorkloadProperties("C++")
java = WorkloadProperties("Java")
tls = WorkloadProperties("TLS")
ui = WorkloadProperties("UI")
fixed_arch = WorkloadProperties("Fixed arch")