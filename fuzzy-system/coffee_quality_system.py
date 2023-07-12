import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Create the input variables
aroma = ctrl.Antecedent(np.arange(0, 11, 1), 'aroma')
aftertaste = ctrl.Antecedent(np.arange(0, 11, 1), 'aftertaste')
acidity = ctrl.Antecedent(np.arange(0, 11, 1), 'acidity')

# Create the output variable
quality = ctrl.Consequent(np.arange(0, 101, 1), 'quality')

# Define the membership functions for each input variable
aroma['low'] = fuzz.trimf(aroma.universe, [0, 0, 5])
aroma['medium'] = fuzz.trimf(aroma.universe, [0, 5, 10])
aroma['high'] = fuzz.trimf(aroma.universe, [5, 10, 10])

aftertaste['low'] = fuzz.trimf(aftertaste.universe, [0, 0, 5])
aftertaste['medium'] = fuzz.trimf(aftertaste.universe, [0, 5, 10])
aftertaste['high'] = fuzz.trimf(aftertaste.universe, [5, 10, 10])

acidity['low'] = fuzz.trimf(acidity.universe, [0, 0, 5])
acidity['medium'] = fuzz.trimf(acidity.universe, [0, 5, 10])
acidity['high'] = fuzz.trimf(acidity.universe, [5, 10, 10])

# Define the membership functions for the output variable
quality['low'] = fuzz.trimf(quality.universe, [0, 0, 50])
quality['medium'] = fuzz.trimf(quality.universe, [0, 50, 100])
quality['high'] = fuzz.trimf(quality.universe, [50, 100, 100])

# Define the rules
rule1 = ctrl.Rule(aroma['low'] & aftertaste['low'] & acidity['low'], quality['low'])
rule2 = ctrl.Rule(aroma['medium'] & aftertaste['medium'] & acidity['medium'], quality['medium'])
rule3 = ctrl.Rule(aroma['high'] & aftertaste['high'] & acidity['high'], quality['high'])
rule4 = ctrl.Rule(aroma['low'] & aftertaste['high'], quality['medium'])
rule5 = ctrl.Rule(aftertaste['high'] & acidity['medium'], quality['medium'])
rule6 = ctrl.Rule(acidity['low'] & aftertaste['low'] & aroma['high'], quality['medium'])

# Create the control system with the defined rules
quality_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])

# Create a simulator for the control system
quality_simulator = ctrl.ControlSystemSimulation(quality_ctrl)

# Define example input values for aroma, aftertaste, and acidity
aroma_input = 6
aftertaste_input = 8
acidity_input = 9

quality_simulator.input['aroma'] = aroma_input
quality_simulator.input['aftertaste'] = aftertaste_input
quality_simulator.input['acidity'] = acidity_input

# Compute the output quality value
quality_simulator.compute()

# Print the output coffee quality value
print("Coffee Quality:", quality_simulator.output['quality'])
