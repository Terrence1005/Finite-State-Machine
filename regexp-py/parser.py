from py_finite_automaton import *
from py_nfa import *
from py_dfa import *
from string_matcher import *

EPSILON = FiniteAutomaton.EPSILON

def concat(left_nfa, right_nfa):
    n_states = left_nfa.count_states() + right_nfa.count_states() - 1
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))

    res = NFA(state_list, n_states - 1)

    for trans in left_nfa.transitions:
        res.add_transition(trans.t_from, trans.t_to, trans.t_symbol)

    i = left_nfa.count_states() - 1
    for trans in right_nfa.transitions:
        res.add_transition(trans.t_from + i, trans.t_to + i, trans.t_symbol)
    return res


def union(left_nfa, right_nfa):
    n_states = left_nfa.count_states() + right_nfa.count_states() + 2
    f_state = n_states - 1
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))

    res = NFA(state_list, f_state)

    res.add_transition(0, 1, FiniteAutomaton.EPSILON)
    for trans in left_nfa.transitions:
        res.add_transition(trans.t_from + 1, trans.t_to + 1, trans.t_symbol)
    i = left_nfa.count_states()
    res.add_transition(i, f_state, FiniteAutomaton.EPSILON)

    i += 1
    res.add_transition(0, i, FiniteAutomaton.EPSILON)
    for trans in right_nfa.transitions:
        res.add_transition(trans.t_from + i, trans.t_to + i, trans.t_symbol)
    res.add_transition(right_nfa.count_states() + i - 1, f_state, FiniteAutomaton.EPSILON)
    return res


def kleene_star(nfa):
    n_states = nfa.count_states() + 2
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))
    res = NFA(state_list, n_states - 1)

    for trans in nfa.transitions:
        res.add_transition(trans.t_from + 1, trans.t_to + 1, trans.t_symbol)

    res.add_transition(0, 1, EPSILON)
    res.add_transition(0, n_states - 1, EPSILON)
    res.add_transition(n_states - 2, 1, EPSILON)
    res.add_transition(n_states - 2, n_states - 1, EPSILON)

    return res
def zero_or_more(nfa):
    n_states = nfa.count_states() + 1
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))
    res = NFA(state_list, n_states - 1)

    for trans in nfa.transitions:
        res.add_transition(trans.t_from, trans.t_to, trans.t_symbol)

    # res.add_transition(0, 1, EPSILON)
    res.add_transition(0, n_states - 1, EPSILON)
    res.add_transition(n_states - 2, 0, EPSILON)
    # res.add_transition(n_states - 2, n_states - 1, EPSILON)

    return res


def zero_or_one(nfa):
    n_states = nfa.count_states() + 1
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))
    res = NFA(state_list, n_states - 1)

    for trans in nfa.transitions:
        res.add_transition(trans.t_from, trans.t_to, trans.t_symbol)

    res.add_transition(0, n_states - 1, EPSILON)
    res.add_transition(n_states - 2, n_states - 1, EPSILON)

    return res

def one_or_more(nfa):
    n_states = nfa.count_states() + 1
    state_list = []
    for i in range(n_states):
        state_list.append(State('q' + str(i)))
    res = NFA(state_list, n_states - 1)

    for trans in nfa.transitions:
        res.add_transition(trans.t_from, trans.t_to, trans.t_symbol)

    # res.add_transition(0, 1, EPSILON)
    res.add_transition(n_states - 2, 0, EPSILON)
    # res.add_transition(n_states - 1, 0, EPSILON)
    res.add_transition(n_states - 2, n_states - 1, EPSILON)


    return res



def re_to_nfa(regexp):
    __known_operators__ = ['(', ')', '.', '|', '*']
    operands = []
    operators = []
    for symbol in regexp:
        if symbol not in __known_operators__:
            nfa = NFA([State('q0'), State('q1')], 1, [Transition(0, 1, symbol)])
            # append == push
            operands.append(nfa)
        else:
            if symbol == '*':
                star_nfa = operands.pop()
                operands.append(zero_or_more(star_nfa))
            elif symbol == '.':
                operators.append(symbol)
            elif symbol == '|':
                operators.append(symbol)
            elif symbol == '(':
                operators.append(symbol)
            elif symbol == ')':
                op = operators.pop()
                while op != '(':
                    right = operands.pop()
                    left = operands.pop()
                    if op == '.':
                        operands.append(concat(left, right))
                    elif op == '|':
                        operands.append(union(left, right))
                    op = operators.pop()
    return operands.pop()

def main():
    a = NFA()
    b = NFA()

    print '\nFor the regular expression segment : (a)'
    a.add_state('q0')
    a.add_state('q1')
    a.add_transition(0, 1, 'a')
    a.set_final_state(1)
    a.display()

    print '\nFor the regular expression segment : (b)'
    b.add_state('q0')
    b.add_state('q1')
    b.add_transition(0, 1, 'b')
    b.set_final_state(1)
    b.display()

    print '\nFor the regular expression segment [Concatenation] : (a.b)'
    concat(a, b).display()

    print '\nFor the regular expression segment [Or] : (a|b)'
    union(a, b).display()

    print '\nFor the regular expression segment [zero or one] : (a?)'
    zero_or_one(a).display()

    print '\nFor the regular expression segment [zero or more] : (a*)'
    zero_or_more(a).display()

    print '\nFor the regular expression segment [one or more] : (a+)'
    one_or_more(a).display()

    print '\nExample 1 NFA : a.(a|b)'
    nfa = concat(a, union(a, b))
    nfa.display()
    print '\nExample 1 DFA : a.(a|b)'
    dfa = DFA()
    dfa.from_nfa(nfa)
    dfa.display()

    print '\nExample 2 NFA : a.(a|b).b+'
    nfa = concat(concat(a, union(a, b)), one_or_more(b))
    nfa.display()
    print '\nExample 2 DFA : a.(a|b).b+'
    dfa = DFA()
    dfa.from_nfa(nfa)
    dfa.display()

    # re = '(1.(((0.0)*)|0).1)'
    # print '\nExample 2 : ' + re
    # matcher = StringMatcher(re)
    # source = '010110101111000110101101001010001011101101110100001000101010101011001010100101001001011010101100100001111'
    # matcher.match_agaisnt(source)

    # state_list = []
    # for i in range(6):
    #     state_list.append(State('q' + str(i)))
    # test_nfa = NFA(state_list, 5)
    # _e_ = FiniteAutomaton.EPSILON
    # test_nfa.add_transition(0, 1, _e_)
    # test_nfa.add_transition(0, 5, _e_)
    # test_nfa.add_transition(1, 2, '1')
    # test_nfa.add_transition(2, 3, _e_)
    # test_nfa.add_transition(3, 4, 0)
    # test_nfa.add_transition(4, 1, _e_)
    # test_nfa.add_transition(4, 5, _e_)
    # test_nfa.table.display()
    # dfa = DFA()
    # dfa.from_nfa_table(test_nfa.table)



    # print '\nExample 3 : (1.(0*).1)'
    # re_to_nfa('(1.(0*).1)').display()


if __name__ == '__main__':
    main()
