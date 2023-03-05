from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the structure of the Bayesian network
model = BayesianNetwork([('E', 'SH'), ('E', 'SE'), ('P', 'SH'), ('P', 'SE')])

# Define the variables
e_states = ['True', 'False']
p_states = ['A', 'B']
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
    variable_card=2,
    values=[[0.5], [0.5]],
    state_names={'P': p_states}
)

# Define the CPT for SE given E and P
se_cpt = TabularCPD(
    variable='SE',
    variable_card=3,
    evidence=['E', 'P'],
    evidence_card=[2, 2],
    values=[
        # first column is E is true and Party is A,
        # second column is E is true and Party is B
        # etc.
        [0.33, 0.15, 0.89, 0.89],  # SE (low)
        [0.33, 0.15, 0.1, 0.1],  # SE (moderate)
        [0.33, 0.7, 0.01, 0.01],  # SE (high)
    ],
    state_names={'SE': se_states, 'E': e_states, 'P': p_states}
)

# Define the CPT for SH given E and P
sh_cpt = TabularCPD(
    variable='SH',
    variable_card=3,
    evidence=['E', 'P'],
    evidence_card=[2, 2],
    values=[
        # first column is E is true and Party is A,
        # second column is E is true and Party is B
        # etc.
        [0.05, 0.33, 0.89, 0.89],  # SH (low)
        [0.15, 0.33, 0.1, 0.1],  # SH (moderate)
        [0.8, 0.33, 0.01, 0.01],  # SH (high)
    ],
    state_names={'SH': sh_states, 'E': e_states, 'P': p_states}
)

model.add_cpds(e_cpt, p_cpt, se_cpt, sh_cpt)


# Create the variable elimination object
infer = VariableElimination(model)

# Compute the probability
prob = infer.query(['P'], evidence={'SE': 'high', 'SH': 'moderate', 'E': 'True'})

print('Probability table of all parties given SE=High, SH=moderate, E=True ', prob, '\n')

print('Party B has highest probability even when party C does not field any candidate ', prob.values[1])