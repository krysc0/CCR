from gurobipy import Model, GRB

weights = [2, 3, 4, 5, 1]
reward = [3, 4, 5, 6, 2]
capacity = 10
n = len(weights)

# Create a new model
model = Model("knapsack")

x = model.addVars(n, vtype=GRB.BINARY, name="x")

# Set the objective: maximize the total reward
model.setObjective(sum(reward[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

# Add constraint: total weight must not exceed capacity
model.addConstr(sum(weights[i] * x[i] for i in range(n)) <= capacity, "capacity")

# Optimize the model
model.optimize()

# Output the solution
if model.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {model.objVal}")
    selected_items = [i for i in range(n) if x[i].x == 1]
    print(f"Selected items: {selected_items}")