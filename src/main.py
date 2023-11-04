#!/bin/python3
'''
CS 341-005
Benedikt Macaro
DPDA simulator
'''

class DPDA:
    """
    Class representation of DPDA
    Q: number of states
    SIG: language alphabet
    GAM: stack alphabet
    F: accept states

    d: transitions for each state
    stack: dpda stack memory
    """
    def __init__(self):
        self.Q = -1
        self.SIG = -1
        self.GAM = set('$')
        self.F = -1
        
        self.d = {}
        self.stack = []

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

    def print_transitions(self, q):
        print("Transitions for state {}:".format(q))
        if (q in self.d):
            for n in self.d[q]:
                a = n[0]
                t = n[1]
                w = n[3]
                if (a == "-"):
                    a = "eps"
                if (t == "-"):
                    t = "eps"
                if (w == "-"):
                    w = "eps"
                print("[{0},{1}->{2}]".format(a, t, w))
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
                    break
                elif (tmp == "y"):
                    trans = self.get_transition(i)
                    if (trans):
                        self.add_transition(i, trans)
                    else:
                        print("did not add")
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
        case = self.valid(q, (a, t, r, w, c))
        if (case == 0):
            return (a, t, r, w, c)
        print("Invalid transition!")
        #TODO: Specific error msg based on condition violation
        return False

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
        c = trans[4]
        if (q not in self.d):
            return 0

        if (c == 1):
            if (q in self.d):
                return 1

        elif (c == 2):
            for t in self.d[q]:
                if (t[4] == 1 or t[1] == trans[1]):
                    return 2

        elif (c == 3):
            for t in self.d[q]:
                if (t[4] == 1 or t[0] == trans[0]):
                    return 3

        elif (c == 4):
            for t in self.d[q]:
                if (t[4] == 1 or (t[0] == trans[0] or t[1] == trans[1])):
                    return 4
        else:
            print("how did we get here")
            return 5
        return 0

def main():
    M = DPDA()
    M.set_init()
    M.get_all_transitions()
    M.print_all_transitions()

if __name__ == '__main__':
    main();
