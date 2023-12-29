from finite_automata import DFA, NFA, test_equivalence

# dfa that accepts b*aa*
example_dfa = DFA(
    states = {0, 1, 2},
    alphabet = {'a', 'b'},
    transition = {
        0: {'a': 1, 'b': 0},
        1: {'a': 1, 'b': 2},
        2: {'a': 2, 'b': 2}
    },
    start = 0,
    accept = {1}
)

example_nfa = example_dfa.to_nfa()

example_strings = [
    'abba',
    'aaaa',
    'bbbb',
    'bbaa',
    'bbbbbbbbbaa',
    'aa',
    'a',
    'b'
]

print(test_equivalence(example_dfa, example_nfa, example_strings))

# nfa that accepts (010 + 01)*
example_nfa = NFA(
    states = {0, 1, 2},
    alphabet = {'0', '1'},
    transition = {
        0: {'0': {1}},
        1: {'1': {2}},
        2: {'0': {0}}
    },
    epsilon = {
        2: {0}
    },
    start = 0,
    accept = {0}
)

example_dfa = example_nfa.to_dfa()

# pprint(example_dfa.transition)

example_strings = [
    '0',
    '1',
    '11',
    '00',
    '01',
    '010',
    '01011',
    '010',
    '010011',
    '01010100101',
]

print(test_equivalence(example_dfa, example_nfa, example_strings))

# string must always contain 1
# if 00 is in the string, there shoule be a 1 somewhere before it
wee_nfa = NFA(
    states = {'a', 'b', 'c', 'd', 'e'},
    alphabet = {'0', '1'},
    transition = {
        'a': {'0': {'b', 'c'}, '1': {'d'}},
        'b': {'1': {'d', 'e', 'c'}},
        'c': {'0': {'e', 'c'}},
        'd': {'0': {'d'}, '1': {'d', 'b'}},
        'e': {'1': {'c'}}
    },
    epsilon = {
        'd': {'e'}
    },
    start = 'a',
    accept = {'d'}
)

example_strings = [
    '0',
    '1',
    '11',
    '00',
    '01',
    '010',
    '01011',
    '0010',
    '010011',
    '001010100101',
    '0101010011001',
]

wee_dfa = wee_nfa.to_dfa()

from pprint import pprint
pprint(wee_dfa.transition)

print(test_equivalence(example_dfa, example_nfa, example_strings))
