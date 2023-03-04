from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Define the structure of the Bayesian network
model = BayesianNetwork([('E', 'SH'), ('E', 'SE'), ('P', 'SH'), ('P', 'SE')])

# Define the variables
e_states = ['True', 'False']
p_states = ['A', 'B', 'C']
sh_states = ['low', 'moderate', 'high']
se_states = ['low', 'moderate', 'high']


# Define the CPT for E
e_cpt = TabularCPD(
    variable='E',
    variable_card=2,
    values=[[0.5],[0.5]],
    state_names={'E': e_states}
)

# Define the CPT for P
p_cpt = TabularCPD(
    variable='P',
    variable_card=3,
    values=[[0.33], [0.33], [0.33]],
    state_names={'P': p_states}
)

# Define the CPT for SE given E and P
se_cpt = TabularCPD(
    variable='SE',
    variable_card=3,
    evidence=['E', 'P'],
    evidence_card=[2, 3],
    values=[
        # first column is E is true and Party is A,
        # second column is E is true and Party is B
        # etc.
        [0.33, 0.15, 0.2, 0.89, 0.89, 0.89],  # SE (low)
        [0.33, 0.15, 0, 0.1, 0.1, 0.1],  # SE (moderate)
        [0.33, 0.7, 0.8, 0.01, 0.01, 0.01],  # SE (high)
    ],
    state_names={'SE': se_states, 'E': e_states, 'P': p_states}
)

# Define the CPT for SH given E and P
sh_cpt = TabularCPD(
    variable='SH',
    variable_card=3,
    evidence=['E', 'P'],
    evidence_card=[2, 3],
    values=[
        # first column is E is true and Party is A,
        # second column is E is true and Party is B
        # etc.
        [0.05, 0.33, 0.2, 0.89, 0.89, 0.89],  # SH (low)
        [0.15, 0.33, 0, 0.1, 0.1, 0.1],  # SH (moderate)
        [0.8, 0.33, 0.8, 0.01, 0.01, 0.01],  # SH (high)
    ],
    state_names={'SH': sh_states, 'E': e_states, 'P': p_states}
)

model.add_cpds(e_cpt, p_cpt, se_cpt, sh_cpt)

# Create a directed graph object
graph = nx.DiGraph()

# Add edges from the Bayesian model to the directed graph
graph.add_edges_from(model.edges())

# Draw the directed graph
nx.draw(graph, with_labels=True)
plt.show()
