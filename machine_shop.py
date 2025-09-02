import gurobipy as gp
from gurobipy import GRB

M = ['p', 'l']

profit = {'p': 100, 'l': 150}
purchase = {'p': 8000, 'l': 4000}
space = {'p': 15, 'l': 30}

total_purchase = 40000
total_space = 200


class BranchAndBoundNode:
    def __init__(self, node_id, constraints=None):
        self.node_id = node_id
        self.constraints = constraints or []
        self.upper_bound = None
        self.lower_bound = None
        self.solution = {}
        self.integer_solution = {}
        self.is_feasible = True
        self.is_integer = False


def solve_relaxed_problem(constraints=None):

    m = gp.Model("machine_shop_relaxed") # first we need to solve the relaxed lp problem
    m.setParam('OutputFlag', 0)  # hide the output window

    x = m.addVars(M, vtype=GRB.CONTINUOUS, name="x") # define the variable

    # Define the objective function
    objective = gp.quicksum(profit[i] * x[i] for i in M)
    m.setObjective(objective, GRB.MAXIMIZE)

    # Original constraints
    m.addConstr(gp.quicksum(purchase[i] * x[i] for i in M) <= total_purchase, name="purchase")
    m.addConstr(gp.quicksum(space[i] * x[i] for i in M) <= total_space, name="floor_space")

    # Additional branching constraints
    if constraints:
        for i, (var, operator, value) in enumerate(constraints):
            if operator == '<=':
                m.addConstr(x[var] <= value, name=f"branch_{i}")
            elif operator == '>=':
                m.addConstr(x[var] >= value, name=f"branch_{i}")

    # Solve
    m.optimize()

    if m.Status == GRB.OPTIMAL:
        solution = {i: x[i].x for i in M}
        return m.ObjVal, solution, True
    else:
        return None, {}, False


def is_integer_solution(solution, tolerance=1e-6):
    # need to check whether the solution has integer solution
    return all(abs(solution[i] - round(solution[i])) < tolerance for i in M)


def get_fractional_parts(solution):
    return {i: solution[i] - int(solution[i]) for i in M} # extract the fractional part of the solution


def select_branching_variable(solution):
    fractional_parts = get_fractional_parts(solution) # get the biggest fractional soltuion
    return max(fractional_parts.keys(), key=lambda x: fractional_parts[x])


def calculate_integer_lower_bound(solution):
    integer_values = {i: int(solution[i]) for i in M} # calculate lower bound
    return sum(profit[i] * integer_values[i] for i in M)


def branch_and_bound():
    print("Starting Branch and Bound Algorithm") # main branch and bound algorithm
    print("=" * 50)

    # Node counter and list
    node_counter = 1
    nodes_to_process = []
    processed_nodes = []

    # Step 1: Solve initial relaxed problem
    print(f"Node {node_counter}: Initial relaxed problem")
    obj_val, solution, feasible = solve_relaxed_problem()

    if not feasible:
        print("Initial problem is infeasible!")
        return None

    # Create initial node
    initial_node = BranchAndBoundNode(node_counter)
    initial_node.upper_bound = obj_val
    initial_node.solution = solution
    initial_node.lower_bound = calculate_integer_lower_bound(solution)
    initial_node.integer_solution = {i: int(solution[i]) for i in M}
    initial_node.is_integer = is_integer_solution(solution)

    print(f"  Upper bound: {initial_node.upper_bound:.2f} (x_p={solution['p']:.2f}, x_l={solution['l']:.2f})")
    print(
        f"  Lower bound: {initial_node.lower_bound:.2f} (x_p={initial_node.integer_solution['p']}, x_l={initial_node.integer_solution['l']})")

    processed_nodes.append(initial_node)

    if initial_node.is_integer:
        print("  → Integer solution found at root node!")
        return initial_node

    # Add to processing queue
    nodes_to_process.append(initial_node)
    current_best_integer_solution = initial_node
    node_counter += 1

    # Now second step is to Branch and bound loop
    while nodes_to_process:
        # Select node with highest upper bound
        current_node = max(nodes_to_process, key=lambda n: n.upper_bound)
        nodes_to_process.remove(current_node)

        print(f"\nBranching from Node {current_node.node_id}")

        # Select branching variable
        branch_var = select_branching_variable(current_node.solution)
        branch_val = int(current_node.solution[branch_var])

        fractional_parts = get_fractional_parts(current_node.solution)
        print(f"  Branching on {branch_var} (fractional part: {fractional_parts[branch_var]:.2f})")
        print(f"  Creating constraints: {branch_var} ≤ {branch_val} and {branch_var} ≥ {branch_val + 1}")

        # Create two child nodes
        for constraint_type, constraint_val in [('<=', branch_val), ('>=', branch_val + 1)]:
            print(f"\n  Node {node_counter}: {branch_var} {constraint_type} {constraint_val}")

            # Create new constraints list
            new_constraints = current_node.constraints.copy()
            new_constraints.append((branch_var, constraint_type, constraint_val))

            # Solve subproblem
            obj_val, solution, feasible = solve_relaxed_problem(new_constraints)

            if feasible:
                new_node = BranchAndBoundNode(node_counter, new_constraints)
                new_node.upper_bound = obj_val
                new_node.solution = solution
                new_node.is_integer = is_integer_solution(solution)

                if new_node.is_integer:
                    new_node.lower_bound = obj_val
                    new_node.integer_solution = {i: int(solution[i]) for i in M}
                else:
                    new_node.lower_bound = current_best_integer_solution.lower_bound
                    new_node.integer_solution = current_best_integer_solution.integer_solution.copy()

                print(f"    Upper bound: {new_node.upper_bound:.2f} (x_p={solution['p']:.2f}, x_l={solution['l']:.2f})")
                print(f"    Lower bound: {new_node.lower_bound:.2f}")

                # Check if this is the best integer solution found
                if new_node.is_integer and new_node.upper_bound > current_best_integer_solution.lower_bound:
                    current_best_integer_solution = new_node
                    print(f"    → New best integer solution!")

                processed_nodes.append(new_node)

                # Add to queue for further branching if not integer and bound is promising
                if not new_node.is_integer and new_node.upper_bound > current_best_integer_solution.lower_bound:
                    nodes_to_process.append(new_node)
                elif new_node.upper_bound <= current_best_integer_solution.lower_bound:
                    print(
                        f"    → Pruned (bound {new_node.upper_bound:.2f} ≤ {current_best_integer_solution.lower_bound:.2f})")

            else:
                print(f"    → Infeasible")

            node_counter += 1

    print("\n" + "=" * 50)
    print("OPTIMAL SOLUTION FOUND")
    print("=" * 50)
    print(f"Optimal objective value: {current_best_integer_solution.lower_bound:.2f}")
    print(
        f"Solution: x_p = {current_best_integer_solution.integer_solution['p']}, x_l = {current_best_integer_solution.integer_solution['l']}")
    print(f"Total nodes processed: {len(processed_nodes)}")

    return current_best_integer_solution


def print_solution_interpretation(optimal_node):
    if optimal_node:
        print("\n" + "=" * 50)
        print("SOLUTION INTERPRETATION")
        print("=" * 50)
        sol = optimal_node.integer_solution
        print(f"Purchase {sol['p']} presses and {sol['l']} lathes")
        print(f"Daily profit increase: ${optimal_node.lower_bound:.2f}")

        # Verify constraints
        cost = purchase['p'] * sol['p'] + purchase['l'] * sol['l']
        space_used = space['p'] * sol['p'] + space['l'] * sol['l']
        print(f"\nResource usage:")
        print(f"Cost: ${cost:,} / ${total_purchase:,} (${total_purchase - cost:,} remaining)")
        print(f"Space: {space_used} ft² / {total_space} ft² ({total_space - space_used} ft² remaining)")


if __name__ == "__main__":
    optimal_solution = branch_and_bound()
    print_solution_interpretation(optimal_solution)