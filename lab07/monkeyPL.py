from .PL import sVariable, sNeg, sAnd, sOr, sConjunction, sDisjunction, sIfOnlyIf, sImplies, bruteForceSAT
from typing import List, Set, Dict
import time


########## PARAMETERS OF THE ENVIRONMENT ##########

n = 2
bananaPosition = 1
initial_box_position = 1

T = 3 # Horizon

########## REPRESENTATION OF THE ENVIRONMENT ##########


# Atemporal variables: Position of the banana

bananaVariables = []  # Contains the list of all banana position variables. Not used as a rule!
B = [] # Contains the knowledge about the position of the banana

for x in range(n):
    pos_var_x = sVariable("B[{x}]".format(x=x))
    bananaVariables.append(pos_var_x)
    
    # TODO: Question 8
    # Fill B with appropriate sentences, in such a way that B[x] indicates whether the banana is located in cell x
    


# Creating action variables

actionVariables = []
for t in range(T):
    actions_t = {'Left' : sVariable("Left_{t}".format(t=t)),
               'Right': sVariable("Right_{t}".format(t=t)),
               'Interact': sVariable("Interact_{t}".format(t=t)),
               'Grab': sVariable("Grab_{t}".format(t=t))}
    actionVariables.append(actions_t)


# Successor-state axioms

# (1) Box position

def boxPositionsAtTime(t: int) -> List:
    return [sVariable("P[{x}]_{t}".format(x=x, t=t)) for x in range(n)]

box_positions = [boxPositionsAtTime(0)] # Contains the list of all box position variables (for now only at time 0, will get incremented). Not used as a rule!

SSA_pos = [] # Successor-state axioms for the position of the box

for t in range(T-1):
    box_positions.append(boxPositionsAtTime(t+1)) 
    # Conditions for being in 0 at time t+1
    conditions = [ sAnd(box_positions[t][1], actionVariables[t]['Left']), # Was in 1 and moved left
                  sAnd(box_positions[t][0], sDisjunction([actionVariables[t]['Left'],   # Was in 0 and moved left
                                                          actionVariables[t]['Interact'],  # Was in 0 and interacted with the box
                                                          actionVariables[t]['Grab']])),  # Was in 0 and grabbed
                  ]
    SSA_pos.append( sIfOnlyIf(box_positions[t+1][0], sDisjunction(conditions)) )
    
    
    
    # Conditions for being in x at time t+1
    
    for x in range(1,n-1):
        conditions = [sAnd(box_positions[t][x-1], actionVariables[t]['Right']), # Was in x-1 and moved right
                      sAnd(box_positions[t][x+1], actionVariables[t]['Left']), # Was in x+1 and moved left
                      sAnd(box_positions[t][x], sDisjunction([actionVariables[t]['Interact'],  # Was in x and interacted with the box
                                                              actionVariables[t]['Grab']])),  # Was in x and grabbed
                      ]
        
        SSA_pos.append( sIfOnlyIf(box_positions[t+1][x], sDisjunction(conditions)) )
        
    
    
    # Conditions for being in n-1 at time t+1
    conditions = [ sAnd(box_positions[t][n-2], actionVariables[t]['Right']), # Was in n-2 and moved right
                  sAnd(box_positions[t][n-1], sDisjunction([actionVariables[t]['Right'],   # Was in n-1 and moved right
                                                            actionVariables[t]['Interact'],  # Was in n-1 and interacted with the box
                                                            actionVariables[t]['Grab']])),  # Was in n-1 and grabbed
                  ]
    SSA_pos.append( sIfOnlyIf(box_positions[t+1][n-1], sDisjunction(conditions)) )
    

# (2) Monkey up

monkey_up = [sVariable("Up_{t}".format(t=t)) for t in range(T)] # Contains the list of all variables for the vertical position of the monkey. Not used as a rule!

SSA_up = [] # Successor-state axioms for the vertical position of the monkey

for t in range(T-1):
    # Conditions for being on the box at time t+1
    
    # TOOD: Question 10: Implement the conditions for being on the box at time t+1
    conditions = [ ]
    
    SSA_up.append( sIfOnlyIf(monkey_up[t+1], sDisjunction(conditions)) )

    

# (3) Grabbing

grabbing_banana = [sVariable("GrabbingBanana_{t}".format(t=t)) for t in range(T)] #  Contains the list of all variables about grabbing the banana. Not used as a rule!
SSA_banana = [] # Successor-state axioms about whether the monkey is grabbing the banana

for t in range(T-1):
    # Conditions for grabbing the banana at time t+1
    
    # TOOD: Question 11: Implement the conditions for grabbing the banana at time t+1
    conditions = [ ]
    SSA_banana.append( sIfOnlyIf(grabbing_banana[t+1], sDisjunction(conditions)) )
    
    
# Constraints axioms on actions

CA_actions = []

for t in range(T-1):
    actions_t = [actionVariables[t][a] for a in actionVariables[t]]
    
    unique_action_vs_others = [(elem, actions_t[:i] + actions_t[i+1:]) for i, elem in enumerate(actions_t)]
    CA_actions += [sImplies(u[0], sConjunction([ sNeg(a) for a in u[1] ])) for u in unique_action_vs_others]
    
    

# Constraints axioms on positions

CA_positions = []

for t in range(T-1):
    positions_t = box_positions[t]
    
    #unique_position_vs_others = [(elem, positions_t[:i] + positions_t[i+1:]) for i, elem in enumerate(positions_t)]
    #CA_positions += [sImplies(u[0], sConjunction([ sNeg(a) for a in u[1] ])) for u in unique_position_vs_others]
    
    for x in range(n):
        CA_positions += [ sOr(sNeg(positions_t[x]), sNeg(positions_t[y])) for y in range(n) if y != x]



# Constraints on action feasibility

CA_feasibility = [ sImplies(monkey_up[t], sConjunction([sNeg(actionVariables[t]['Right']),
                                                        sNeg(actionVariables[t]['Left'])
                                                        ])) for t in range(T-1)]



########## REPRESENTATION OF THE SEARCH PROBLEM ##########

# Initial state

# TODO: Question 13: Implement the description of the initial state
init = []


# Goal

# TODO: Question 14: Implement the description of the goal
goal = []





########## SOLVING THE SEARCH PROBLEM ##########


# TODO: Question 15: Use the brute force SAT solver to find a solution to the search problem

problem_sentences = B + SSA_pos + SSA_up + SSA_banana + CA_actions + CA_positions + CA_feasibility + init + goal
problem = sConjunction(problem_sentences)


start_time = time.time()

instantiation = bruteForceSAT(problem)

end_time = time.time()

print("Execution time:", end_time - start_time, "seconds")



