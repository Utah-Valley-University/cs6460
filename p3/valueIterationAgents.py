# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import math
import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        ''' This function implements the Bellman Update Equation of AIMA 4 17.10.
        It uses batch update, meaning we update all state values at time k+1 using
        time k values versus updating one value at a time and using the new values.
        '''
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        Q = self.computeQValueFromValues
        A = self.mdp.getPossibleActions
        S = self.mdp.getStates
        
        for _ in range(self.iterations):
            new_values = util.Counter()
            for state in S():
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    U = max([Q(state,a) for a in A(state)])
                    new_values[state] = U
            self.values = new_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        R = self.mdp.getReward
        P = self.mdp.getTransitionStatesAndProbs

        q_value = sum([probability * (R(state, action,None) + self.discount * self.values[s_prime]) for s_prime, probability in P(state, action)])
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        q_value, max_action = max([(self.computeQValueFromValues(state, action), action) for action in actions])
        return max_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()

        for iteration in range(self.iterations):
            state  = states[iteration % len(states)]
            if self.mdp.isTerminal(state):
                continue
            actions = self.mdp.getPossibleActions(state)
            q_value = max([self.getQValue(state,action) for action in actions])
            self.values[state] = q_value


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        ''' Numbers refer to steps from the project description pseudocode '''

        S = self.mdp.getStates
        A = self.mdp.getPossibleActions
        P = self.mdp.getTransitionStatesAndProbs
        Q = self.computeQValueFromValues
        G = self.mdp.isTerminal
        
        #2 priority queue
        p_queue = util.PriorityQueue()

        #1 find all predecessors
        predecessors = {}
        for state in S():
            if not G(state):
                for action in A(state):
                    for s_prime, probability in P(state, action):
                        '''
                        if s_prime in predecessors:
                            predecessors[s_prime].add(state)
                        else:
                            predecessors[s_prime] = {state}
                        '''
                        states = predecessors.get(s_prime, set())
                        states.add(state)
                        predecessors[s_prime] = states
                        
        #3 compute diffs for non-terminal states                
        for state in S():
            if not G(state):
                diff = abs(self.values[state] - max([Q(state, action) for action in A(state)]))
                p_queue.update(state, -diff)

        #4 iterations
        for iteration in range(self.iterations):
            #4a
            if p_queue.isEmpty():
                break
            #4b
            state = p_queue.pop()
            #4c
            if not G(state):
                self.values[state] = max([Q(state, action) for action in A(state)])
            #4d
            for p in predecessors[state]:
                #4d.i
                if not G(p):
                    diff = abs(self.values[p] - max([Q(p, action) for action in A(p)]))
                    #4d.ii
                    if diff > self.theta:
                            p_queue.update(p, -diff)
