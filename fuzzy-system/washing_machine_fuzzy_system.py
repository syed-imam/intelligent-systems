# -*- coding: utf-8 -*-

# -- Sheet --

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

from skfuzzy import control as ctrl

## INPUT VARIABLES
# load_size, dirt_level, clothes_type

# Load size
load_size_range = np.arange(0, 201, 20) # Range will be 0 to 200 pounds
load_size = ctrl.Antecedent(load_size_range, 'load_size')

# Lower bound is 0, peak height is at 0, and upper bound is 40 
load_size['small'] = fuzz.trimf(load_size.universe, [0, 0, 40])
# # Lower bound is 30, peak height is at 50, and upper bound is 70
load_size['medium'] = fuzz.trimf(load_size.universe, [30, 50, 70])
# # Lower bound is at 60, peak height is at 140, and upper bound is 200 
load_size['large'] = fuzz.trimf(load_size.universe, [60, 140, 200])

# plot the membership function
load_size.view()


# Dirt level
dirt_level_range = np.arange(0, 101, 10)
dirt_level = ctrl.Antecedent(dirt_level_range, 'dirt_level')

dirt_level['low'] = fuzz.trimf(dirt_level.universe, [0, 20, 40]) 
dirt_level['medium'] = fuzz.trimf(dirt_level.universe, [40, 60, 70])
dirt_level['high'] = fuzz.trimf(dirt_level.universe, [60, 80, 100])

# plot the membership function
dirt_level.view()

# Clothes type
clothes_type_range = np.arange(0, 11, 1)
clothes_type = ctrl.Antecedent(clothes_type_range, 'clothes_type')

clothes_type['soft'] = fuzz.trimf(clothes_type.universe, [0, 1, 5]) 
clothes_type['normal'] = fuzz.trimf(clothes_type.universe, [4, 5, 8])
clothes_type['heavy'] = fuzz.trimf(clothes_type.universe, [7, 8, 10])

# plot the membership function
clothes_type.view()


## OUTPUT VARIABLES
# Wash time

# wash time range is 0 to 10 minutes
wash_time_range = np.arange(0, 11, 1) 
wash_time = ctrl.Consequent(wash_time_range, 'wash_time')

wash_time['short'] = fuzz.trimf(wash_time.universe, [0, 2, 4])
wash_time['medium'] = fuzz.trimf(wash_time.universe, [3, 5, 7])
wash_time['long'] = fuzz.trimf(wash_time.universe, [7, 9, 10])

wash_time.view()


## RULES
rule1 = ctrl.Rule(dirt_level['high'] & load_size['large'], wash_time['long'])
rule2 = ctrl.Rule(dirt_level['low'] & load_size['small'], wash_time['short'])
rule3 = ctrl.Rule(dirt_level['medium'] & load_size['small'], wash_time['short'])
rule4 = ctrl.Rule(clothes_type['soft'], wash_time['short'])
rule5 = ctrl.Rule(clothes_type['heavy'], wash_time['long'])
rule6 = ctrl.Rule(load_size['large'] | clothes_type['heavy'], wash_time['long'])


washing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
simulation = ctrl.ControlSystemSimulation(washing_ctrl)

# INPUT SET 1
simulation.input['load_size'] = 170
simulation.input['dirt_level'] = 60
simulation.input['clothes_type'] = 7
simulation.compute()

# Access the result of the control system
print("Result: 1 ", simulation.output['wash_time'])

wash_time.view(sim=simulation)

# INPUT SET 2
simulation.input['load_size'] = 40
simulation.input['dirt_level'] = 80
simulation.input['clothes_type'] = 1
simulation.compute()

# Access the result of the control system
print("Result: 2 ", simulation.output['wash_time'])

# INPUT SET 3
simulation.input['load_size'] = 120
simulation.input['dirt_level'] = 90
simulation.input['clothes_type'] = 9
simulation.compute()

# Access the result of the control system
print("Result: 3 ", simulation.output['wash_time'])

