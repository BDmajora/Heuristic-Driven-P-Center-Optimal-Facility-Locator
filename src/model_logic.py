import pulp

class PCenterSolver:
    def __init__(self, nodes, distances, p_count, weights):
        self.nodes = nodes
        self.distances = distances
        self.p_count = p_count
        self.weights = weights 

    def solve(self):
        # Create the optimization problem
        prob = pulp.LpProblem("Hospital_Placement", pulp.LpMinimize)
        
        # y[node]: 1 if hospital is built at node, 0 if not
        y = pulp.LpVariable.dicts("Hospital", self.nodes, cat=pulp.LpBinary)
        
        # x[demand][hospital]: 1 if demand node is served by hospital node
        x = pulp.LpVariable.dicts("Service", (self.nodes, self.nodes), cat=pulp.LpBinary)
        
        # Variable for the longest travel distance in the sample
        z = pulp.LpVariable("MaxDistance", lowBound=0, cat=pulp.LpContinuous)
        
        # Objective: minimize the maximum distance value
        prob += z
        
        # Constraint: total hospitals must equal p_count
        prob += pulp.lpSum([y[j] for j in self.nodes]) == self.p_count
        
        for i in self.nodes:
            # Constraint: each node must connect to exactly one hospital
            prob += pulp.lpSum([x[i][j] for j in self.nodes]) == 1
            
            for j in self.nodes:
                # Constraint: node cannot be served by a non-existent hospital
                prob += x[i][j] <= y[j]
            
            # Constraint: z must be at least the distance of each assignment
            prob += self.weights[i] * pulp.lpSum([self.distances[i, j] * x[i][j] for j in self.nodes]) <= z
        # Run the solver without terminal logs
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Identify node IDs where hospitals were placed
        hospital_nodes = [n for n in self.nodes if pulp.value(y[n]) == 1]
        
        # Final calculation of the worst-case travel distance
        max_dist = pulp.value(z)
        
        return hospital_nodes, max_dist