# I think the general format of this is going to be:
#   parse_input()
#   get_items()
#   solve()

# -------------------------------------

# Copied from everyone's favorite LLM
# Example of LP to solve the grocery problem
# I don't know what my interface is going to be yet, take everything here as
# super rough and just an example
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# define data
items = ["milk", "bread", "eggs"]
stores = ["store1", "store2", "store3"]
costs = {
    ("milk", "store1"): 2.0,
    ("milk", "store2"): 2.5,
    ("milk", "store3"): 2.1,
    ("bread", "store1"): 1.0,
    ("bread", "store2"): 1.2,
    ("bread", "store3"): 1.1,
    ("eggs", "store1"): 3.0,
    ("eggs", "store2"): 2.8,
    ("eggs", "store3"): 2.9,
}

# Problem
problem = LpProblem("GroceryOptimization", LpMinimize)

# Variables
x = LpVariable.dicts("x", [(i, j) for i in items for j in stores], cat="Binary")
y = LpVariable.dicts("y", stores, cat="Binary")

# Objective function: Minimize total cost
problem += lpSum(costs[(i, j)] * x[(i, j)] for i in items for j in stores)

# Constraints
# Each item must be bought from one store
for i in items:
    problem += lpSum(x[(i, j)] for j in stores) == 1

# Limit to two stores
problem += lpSum(y[j] for j in stores) <= 2

# Link item purchase to store selection
for i in items:
    for j in stores:
        problem += x[(i, j)] <= y[j]

# Solve
problem.solve()

# Output results
print("Optimal Cost:", problem.objective.value())
for i in items:
    for j in stores:
        if x[(i, j)].value() == 1:
            print(f"Buy {i} from {j}")
