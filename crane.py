from finite_automata import NFA

crane = NFA(
    states={'bottom', 'raising', 'top', 'lowering'},
    alphabet={'0', '1'},
    transition={
        'bottom': {'u': {'bottom'}, 'l': {'bottom'}, 'R': {'raising'}},
        'raising': {'R': {'raising'}},
        'top': {'u': {'top'}, 'l': {'top'}, 'L': {'lowering'}},
        'lowering': {'L': {'lowering'}},
    },
    epsilon={
        'raising': {'raising', 'top'},
        'lowering': {'lowering', 'bottom'},
    },
    start='bottom',
    accept={'bottom'}
)

'''
actions:
    L: lower the crane's hook block to the ground
    u: (optional) unload the hook block
    l: (optional) load the hook block with the load
    R: raise the hook block to the desired height
    u: (optional) unload the hook block
    l: (optional) load the hook block with the load
'''

'''
states:
bottom
raising
top
lowering
'''

print(crane.accepts('lRuL'))  # True
print(crane.accepts('lR'))  # False
