#!/usr/bin/python3
'''
CS 341-005
Benedikt Macaro
DPDA simulator
'''
#TODO:
'''
Code consistency:
- 's' or "s"?
- where to break long strings?
- consistent design?
- strict typing?
- pure functions?
'''

class DPDA:
    """
    Class representation of DPDA
    Q: number of states
    SIG: language alphabet
    GAM: stack alphabet
    F: accept states

    d: transitions for each state
    """
    def __init__(self):
        self.Q = -1
        self.SIG = -1
        self.GAM = set('$')
        self.F = -1
        
        self.d = {}

    def set_init(self):
        """
        Prompts user to set Q, SIG, GAM, F.
        return void
        """
        # TODO: input validation: (ano pa ba?)

        while (self.Q == -1):
            try:
                self.Q = int(input("Enter number of states :\n"))
            except:
                print("Invalid input: number of states must be int")

        while (self.SIG == -1):
            #TODO: allow symbols |a| > 1 ??
            tmp = set(input(
                "Enter input alphabet as a"
                + " comma-separated list of symbols :\n").strip().split(","))
            if ("" in tmp):
                print("Input alphabet can't be empty")
                continue
            if ("$" in tmp):
                print("Can't have '$' as a symbol")
                continue
            if ('-' in tmp):
                print("Can't have '-' as a symbol")
                continue
            self.SIG = tmp

        self.GAM = self.SIG | self.GAM

        while (self.F == -1):
            # For all accept states, delimit by comma, convert to int, store in list.
            try:
                i = set(map(int,
                    input(
                        "Enter accepting states as a "
                        + "comma-separated list of integers :\n").strip().split(",")))

                m = max(i)
                if (m > self.Q - 1):
                    print(
                        "invalid state {0}; enter a value between {1} and {2}"
                        .format(m, 0, self.Q - 1))
                    continue
                self.F = i
            except:
                print("Invalid input: accept state must be integers")
        return

    def trans_to_str(self, tup):
        a = tup[0]
        t = tup[1]
        w = tup[3]
        if (a == "-"):
            a = "eps"
        if (t == "-"):
            t = "eps"
        if (w == "-"):
            w = "eps"
        return "[{0},{1}->{2}]".format(a, t, w)

    def print_transitions(self, q):
        print("Transitions for state {0}:".format(q))
        if (q in self.d):
            for t in self.d[q]:
                print(self.trans_to_str(t))
        return

    def print_all_transitions(self):
        for i in range(self.Q):
            self.print_transitions(i)
        return

    def get_all_transitions(self):
        for i in range(self.Q):
            tmp = -1
            while (tmp != 'y' or tmp != 'n'):
                self.print_transitions(i)
                tmp = input("Need a transition rule for state {0} ? (y or n)"
                            .format(i))
                if (tmp == "n"):
                    # Needed for checking final state in process()
                    if (i not in self.d):
                        # Set the transition to have empty list in dictionary
                        self.d[i] = []
                    break
                elif (tmp == "y"):
                    self.get_transition(i)
                else:
                    print("Invalid input: must be 'y' or 'n'")
        return

    def get_transition(self, q):
        '''
        Prompts user to add transition rule for q.
        Checks if able to add the transition.
        If able, returns tuple (a,t,r,w,c)
        '''
        a, t, r, w, c = -1, -1, -1, -1, -1
        SIG_e = set("-") | self.SIG
        GAM_e = set("-") | self.GAM

        while (a not in SIG_e):
            a = input("Input Symbol to read (enter - for epsilon): ")
            if (a not in SIG_e or len(a) > 1):
                print("Invalid input: symbol not in alphabet")

        while (t not in GAM_e):
            t = input("Stack symbol to match and pop (enter - for epsilon): ")
            if (t not in GAM_e or len(a) > 1):
                print("Invalid input: symbol not in stack alphabet")

        while (r not in range(self.Q)):
            try:
                    r = int(input("State to transition to : "))
                    if (r not in range(self.Q)):
                        print("Invalid input: input greater than", self.Q)
            except:
                print("Invalid input: state must be integer")

        while (w == -1):
            # TODO: Need to make sure stack symbols being pushed are in the alphabet
            tmp = input(
                "Stack symbols to push as comma separated list, "
                + "first symbol to top of stack (enter - for ep"
                + "silon): ")
            tmp_s = set(tmp.replace(",", ""))
            if ("-" in tmp and len(tmp) > 1):
                print("Invalid input: invalid string")
            if (tmp_s & GAM_e == tmp_s):
                w = tmp
            else:
                print("Invalid input: invalid string")

        c = self.condition(a, t)
        if (self.valid(q, (a, t, r, w, c))):
            self.add_transition(q, (a, t, r, w, c))
        return

    def add_transition(self, q, entry):
        if (q not in self.d):
            self.d[q] = [entry]
        else:
            self.d[q].append(entry)
        return
        
    def condition(self, sym_read, stack_top):
        '''
        helper function
        determine which condition for transition being added
        '''
        if (sym_read == '-' and stack_top == '-'):
            return 1
        elif (sym_read == '-' and stack_top != '-'):
            return 2
        elif (sym_read != '-' and stack_top == '-'):
            return 3
        return 4

    def valid(self, q, trans):
        '''
        helper function
        takes in state and tuple.
        Lookup in d for transitions
        compares trans tuple to existing transitions in d
        return 0: valid, not 0: invalid specific errors
        '''
        if (q not in self.d):
            return True

        for t in self.d[q]:
            # The given output is WRONG lmao but this is to match it ;-;
            if (t[4] == 1):
                print("Violation of DPDA due to epsilon input/epsilon"
                      + " stack transition from state {0}:".format(q)
                      + self.trans_to_str(t))
                return False

            elif ((t[0] == trans[0]) and (t[1] == trans[1])):
                print("Violation of DPDA due to multiple transitions"
                      + " for the same input and "
                      + "stack top from state {0}:".format(q)
                      + self.trans_to_str(t))
                return False

            elif ((trans[4] == 1)
                  or (t[0] == trans[0])
                  or (t[1] == trans[1])):
                print("Violation of DPDA due to epsilon stack"
                      + " transition from state {0}:".format(q)
                      + self.trans_to_str(t))
                return False

        return True

def process_s(M, s): 
    '''
    This shit is so messy LMAO
    '''
    stack = []              # DPDA Stack
    curr_s = 0              # DPDA State
    curr_sym = "-"          # Current "token"
    next_sym = ""           # Next "token"
    stack_top = "-"         # Stack top
    configs = ""

    '''
    x1: q_i in F        := In accepting state
    x2: s[i:] == ''     := Done reading input
    x3: stack == []     := Stack is empty
    accept: x1 and x2 and x3
    '''
    x1 = False
    x2 = False
    x3 = True
    accept = False

    # Start computation loop
    i = 0
    while (True):
        # Update configurations string
        configs += "({0};{1};{2})".format(curr_s, s[i:], stack)

        # Update the transitions for the current state
        t = M.d[curr_s]

        # Check the DPDA configuration
        x1 = curr_s in M.F
        x2 = s[i:] == ""
        x3 = len(stack) == 0
        accept = x1 and x2 and x3

        if (accept):
            return (True, configs)

        if (x2 and not (x2 or x3)):
            return (False, configs)

        # Set stream pointer and lookahead
        if (i != len(s)):
            curr_sym = s[i]
        else:
            curr_sym = "-"

        if (i + 1 < len(s)):
            next_sym = s[i + 1]
        else:
            next_sym = "-"

        # Set stack pointer if stack not empty
        if (len(stack) > 0):
            stack_top = stack[-1]
        else:
            stack_top = "-"

        # Choose a transition to make from current state
        for it in t:
            a = it[0]
            t = it[1]
            r = it[2]
            w = it[3]
            c = it[4]

            # First check if eps, eps rule exists or check if input match rule exists
            if (    c == 1 
                    or (c == 3 and curr_sym == a)
                    or (c == 4 and curr_sym == a and stack_top == t)):

                # 1) move to next state
                curr_s = r

                # 2) advance stream pointer if input is matched
                if ((c == 3 or c == 4) and i < len(s)):
                    i += 1

                # 3) update the stack if stack is matched
                if (c == 4):
                    stack.pop()

                # 4) push symbols from transition on to stack
                if (w != "-"):
                    for char in w[::-1]:
                        stack.append(char)

                # 5) update configs with transition taken
                configs += "--[{0},{1}->{2}]-->".format(a, t, w)
                break

            # Next check if skip input read and match stack rule exists
            elif (c == 2 and stack_top == t):
                # 1) move to next state
                curr_s = r

                # 2) update the stack
                stack.pop()

                # 3) push symbols from transition on to stack
                if (w != "-"):
                    for char in w[::-1]:
                        stack.append(char)

                # 4) update configs with transition taken
                configs += "--[{0},{1}->{2}]-->".format(a, t, w)
                break

            # If no transition is possible and there's input to read, stop computation
            elif (x2 and it == t[-1]):
                return (False, configs)

def main():

    # Set up DPDA through user input
    M = DPDA()
    M.set_init()
    M.get_all_transitions()
    M.print_all_transitions()

    # Process input strings through DPDA
    print("\n\n\n")
    print("M.Q:", M.Q)
    print("M.SIG:", M.SIG)
    print("M.GAM:", M.GAM)
    print("M.F:", M.F)
    print("M.d:", M.d)
    s = input("Enter an input string to be processed by the PDA : ")
    ret = process_s(M, s)
    print("Accept string {0}?".format(s), ret[0])
    print(ret[1])
    

if __name__ == '__main__':
    main();
