class DFA:
    def __init__(self, states, alphabet, transition, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start = start
        self.accept = accept

    def accepts(self, string):
        # we just follow the transitions
        state = self.start
        for c in string:
            if c not in self.transition[state]:
                return False
            state = self.transition[state][c]
        return state in self.accept

    def to_nfa(self):
        return NFA(
            states = self.states,
            alphabet = self.alphabet,
            transition = {
                k: {
                    c: {v}
                    for c, v in d.items()
                } for k, d in self.transition.items()
            },
            epsilon = dict(),
            start = self.start,
            accept = self.accept
        )

class NFA:
    def __init__(self, states, alphabet, transition, epsilon, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        # epsilon is a dictionary of state -> set of states reachable by epsilon transition
        # later on, it becomes a dict to lookup epsilon closure for each state
        self.epsilon = epsilon
        self.start = start
        self.accept = accept

        # fix up the epsilon transitions
        for state in self.states:
            if state not in self.epsilon:
                self.epsilon[state] = set()
                continue
            queue = list(self.epsilon[state])
            while queue:
                next = queue.pop()
                if next not in self.epsilon[state]:
                    self.epsilon[state].add(next)
                    queue.extend(self.epsilon[next])

    def accepts(self, string):
        current = set([self.start] + list(self.epsilon[self.start]))
        # print(current)
        for c in string:
            next = set()
            while current:
                state = current.pop()
                if c not in self.transition[state]:
                    continue
                new_states = self.transition[state][c]
                next |= set(new_states)
                for new_state in new_states:
                    next |= self.epsilon[new_state]
            current = next
            # print(current)
        return bool(current & self.accept)

    def to_dfa(self):
        # subset construction
        # create a new DFA with the same alphabet
        alphabet = self.alphabet

        # helper function to get the power set of a set
        def powerset(Q):
            import itertools
            return set(
                frozenset(s) for s in
                    itertools.chain.from_iterable(itertools.combinations(Q, r)
                        for r in range(len(Q) + 1)))
        
        # the states of the DFA are the power set of the states of the NFA
        # we use frozenset because sets are not hashable in Python
        # it's fine to use frozenset because we don't need to modify the states
        states = powerset(self.states)

        # start is E(start) where E is the epsilon closure
        start = frozenset([self.start] + list(self.epsilon[self.start]))
        assert(start in states)

        # the transition function of the DFA is defined as follows:
        # for each state in the DFA, for each character in the alphabet,
        # the transition is the union of the transitions of the NFA
        transition = dict()

        for state in states:
            transition[state] = dict()
            for c in self.alphabet:
                transition[state][c] = set()
                for s in state:
                    if c not in self.transition[s]:
                        continue

                    new_states = self.transition[s][c]
                    transition[state][c] |= new_states
                    for new_state in new_states:
                        # account for epsilon transitions
                        transition[state][c] |= self.epsilon[new_state]

                transition[state][c] = frozenset(transition[state][c])

                # if you have nowhere to go with a character, delete the transition
                if not transition[state][c]:
                    del transition[state][c]

            # if you have nowhere to go from a state, delete the state
            # if not transition[state]:
            #     del transition[state]

        # if there is no way to get to a state from the start state, delete the state
        visited = set()
        queue = [start]
        while queue:
            state = queue.pop()
            if state in visited:
                continue
            visited.add(state)
            for c in alphabet:
                if c not in transition[state]:
                    continue
                queue.append(transition[state][c])

        for state in states:
            if state not in visited:
                del transition[state]

        # the accept states of the DFA are the states that contain an accept state of the NFA
        accept = set()
        for state in states:
            if state & self.accept:
                accept.add(state)
        accept = frozenset(accept)

        return DFA(states, alphabet, transition, start, accept)

def test_equivalence(dfa, nfa, strings):
    for s in strings:
        if dfa.accepts(s) != nfa.accepts(s):
            return False
    return True

