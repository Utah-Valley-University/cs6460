"""multiAgents.py - Multi-Agent Search Algorithms for Pacman
===========================================================

This module implements various multi-agent search algorithms for the Pacman game,
including reflex agents, minimax, alpha-beta pruning, and expectimax search.

The module provides agent classes that:
- Make decisions based on state evaluation functions
- Implement adversarial search algorithms
- Model both deterministic and probabilistic opponent behavior
- Search to configurable depths using evaluation heuristics

Key Classes:
    ReflexAgent: Makes decisions using state evaluation heuristics
    MinimaxAgent: Implements minimax search algorithm
    AlphaBetaAgent: Implements alpha-beta pruning search
    ExpectimaxAgent: Implements expectimax probabilistic search

Usage:
    This module is used by the Pacman game to create AI agents. Agents can be
    selected and configured via command line arguments.

Author: George Rudolph
Date: 14 Nov 2024
Major Changes:
1. Added type hints throughout the codebase for better code clarity and IDE support
2. Improved docstrings with detailed descriptions and Args/Returns sections
3. Enhanced code organization with better function and variable naming

This code runs on Python 3.13

Licensing Information:  You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""

import random, math
import util
from util import manhattanDistance
from game import Agent, Directions
from typing import List, Tuple, Any
from pacman import GameState

class ReflexAgent(Agent):
    """A reflex agent that chooses actions by examining alternatives via a state evaluation function.
    
    This agent evaluates each possible action using a heuristic evaluation function and selects
    among the best options. The evaluation considers factors like:
    - Distance to ghosts (avoiding them)
    - Score improvements
    - Distance to food
    - Maintaining movement direction
    """

    def getAction(self, gameState: GameState) -> str:
        """Choose among the best actions according to the evaluation function.
        
        Args:
            gameState: The current game state
            
        Returns:
            str: A direction from Directions.{North, South, West, East, Stop}
            
        The method collects legal moves, scores them using the evaluation function,
        and randomly selects among those with the best score.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action: str) -> float:
        """Evaluate the desirability of a game state after taking an action.
        
        Args:
            currentGameState: The current game state
            action: The proposed action
            
        Returns:
            float: A score where higher numbers are better, using values 8,4,2,1,0
            that are bitwise orthogonal (powers of 2)
            
        The function evaluates states based on:
        - Avoiding ghosts (returns 0 if too close)
        - Score improvements (returns 8)
        - Getting closer to food (returns 4) 
        - Maintaining direction (returns 2)
        - Default case (returns 1)
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if action == Directions.STOP:
            return 0

        # stay away from ghosts
        distance_2_closest_ghost = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])
        if distance_2_closest_ghost <= 1:
            return 0

        # check for increased score for proposed action
        score_delta = successorGameState.getScore() - currentGameState.getScore()
        if score_delta > 0:
            return 8

        # check if food gets closer
        position = currentGameState.getPacmanPosition()
        distance_2_closest_food = min([manhattanDistance(position, food) for food in currentGameState.getFood().asList()])
        new_distances_2_food = [manhattanDistance(newPos, food) for food in newFood.asList()]
        new_distance_2_closest_food = min(new_distances_2_food, default = 0)
        delta_food = distance_2_closest_food - new_distance_2_closest_food
        if delta_food > 0:
            return 4

        # Keep going in same direction if other criteria not relevant
        direction = currentGameState.getPacmanState().getDirection()
        if action == direction:
            return 2
        
        #default to 1
        return 1


def scoreEvaluationFunction(currentGameState: GameState) -> float:
    """Return the score of the state for use with adversarial search agents.
    
    Args:
        currentGameState: The game state to evaluate
        
    Returns:
        float: The score displayed in the Pacman GUI
        
    This is the default evaluation function for adversarial search agents.
    Not intended for use with reflex agents.
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """Base class for adversarial search agents (minimax, alpha-beta, expectimax).
    
    This abstract class provides common functionality for multi-agent searchers.
    It should not be instantiated directly, but rather extended by concrete
    agent implementations.
    
    Attributes:
        index: Agent index (0 for Pacman)
        evaluationFunction: Function used to evaluate game states
        depth: Maximum depth of search tree
    """

    def __init__(self, evalFn: str = 'scoreEvaluationFunction', depth: str = '2') -> None:
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """Minimax agent that implements adversarial search.
    
    This agent uses minimax search to determine the optimal action by considering
    the worst case scenario at each level.
    """

    def getAction(self, gameState: GameState) -> str:
        """Return the minimax action from the current gameState.
        
        Args:
            gameState: The current game state
            
        Returns:
            str: The optimal action according to minimax search
            
        Uses self.depth and self.evaluationFunction to determine the best action
        by considering the worst-case scenario at each level.
        """

        def min_value(state: GameState, agent_index: int, depth: int) -> float:
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            legal_actions = state.getLegalActions(agent_index)

            # When the last ghost has moved, the next agent is Pacman, otherwise it's another ghost
            if agent_index == state.getNumAgents() - 1:
                return min(max_value(state.generateSuccessor(agent_index, action), depth) for action in legal_actions)
            return min(min_value(state.generateSuccessor(agent_index, action), agent_index + 1, depth) for action in
                           legal_actions)

        def max_value(state: GameState, depth: int) -> float:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            legal_actions = state.getLegalActions(0)
            return max(min_value(state.generateSuccessor(0, action), 1, depth + 1) for action in legal_actions)

        best_action = max(gameState.getLegalActions(0),
                         key=lambda action: min_value(gameState.generateSuccessor(0, action), 1, 1))
        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Minimax agent with alpha-beta pruning optimization.
    
    This agent implements minimax search with alpha-beta pruning to more efficiently
    explore the game tree by pruning branches that cannot affect the final decision.
    """

    def getAction(self, gameState: GameState) -> str:
        """Return the minimax action using alpha-beta pruning.
        
        Args:
            gameState: The current game state
            
        Returns:
            str: The optimal action according to alpha-beta pruning
            
        Pacman is always the max agent, ghosts are always min agents.
        At depth 0, max_value returns an action. At other depths, it returns a value.
        """

        def min_value(state: GameState, agent_index: int, depth: int, alpha: float=-math.inf, beta: float=math.inf) -> float:
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(agent_index)
        
            value = math.inf
            for action in legal_actions:
                next_state = state.generateSuccessor(agent_index, action)

                # If it's the last ghost, then the next agent is Pacman, otherwise it's another ghost
                if agent_index == state.getNumAgents() - 1:
                    new_value = max_value(next_state, depth, alpha, beta)
                else:
                    new_value = min_value(next_state, agent_index + 1, depth, alpha, beta)

                value = min(value, new_value)
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state: GameState, depth: int, alpha: float=-math.inf, beta: float=math.inf) -> Any:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(0)

            if depth == 0:
                value = -math.inf
                for action in legal_actions:
                    next_state = state.generateSuccessor(0, action)
                    new_value = min_value(next_state, 1, depth + 1, alpha, beta)
                    if new_value > value:
                        value = new_value
                        best_action = action
                    alpha = max(alpha, value)
                return best_action  
            else:
                value = -math.inf
                for action in legal_actions:
                    next_state = state.generateSuccessor(0, action)
                    value = max(value, min_value(next_state, 1, depth + 1, alpha, beta))
                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value

        best_action = max_value(gameState, depth=0, alpha=-math.inf, beta=math.inf)
        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """An agent that uses expectimax search to make decisions.
    
    This agent models ghosts as choosing uniformly at random from their legal moves.
    It uses expectimax search to find optimal actions against probabilistic opponents.
    
    The agent searches to a fixed depth using a supplied evaluation function.
    """

    def getAction(self, gameState: GameState) -> str:
        """Return the expectimax action using self.depth and self.evaluationFunction.
        
        Args:
            gameState: The current game state
            
        Returns:
            str: The selected action (one of Directions.{North,South,East,West,Stop})
            
        All ghosts are modeled as choosing uniformly at random from their legal moves.
        """
        def max_value(state: GameState, depth: int) -> float:
            """Calculate the maximum value for Pacman at a given state and depth.
            
            Args:
                state: The current game state
                depth: Current depth in the search tree
                
            Returns:
                float: The maximum value achievable from this state
            """
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(0)
            value = max(exp_value(state.generateSuccessor(0, action), 1, depth + 1) for action in legal_actions)
            return value

        def exp_value(state: GameState, agent_index: int, depth: int) -> float:
            """Calculate the expected value for a ghost at a given state and depth.
            
            Args:
                state: The current game state
                agent_index: Index of the current ghost agent
                depth: Current depth in the search tree
                
            Returns:
                float: The expected value from this state
            """
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(agent_index)
            next_states = [state.generateSuccessor(agent_index, action) for action in legal_actions]
            if agent_index == state.getNumAgents() - 1: #next agent is pacman
                return sum([max_value(next_state, depth) for next_state in next_states])/len(next_states)
            
            return sum([exp_value(next_state, agent_index + 1, depth) for next_state in next_states])/len(next_states)
            
        legal_actions = gameState.getLegalActions(0)
        best_action = max(legal_actions, key=lambda action: exp_value(gameState.generateSuccessor(0, action), 1, 1))
        return best_action

def betterEvaluationFunction(game_state: GameState) -> float:
    """A more sophisticated evaluation function for Pacman game states.
    
    This function evaluates states by combining the game score with a penalty
    based on distance to the closest food pellet. The penalty uses the reciprocal
    of the distance to give higher penalties to food that is farther away.
    
    Args:
        game_state: The game state to evaluate
        
    Returns:
        float: The evaluation score where higher values are better
    """
    position = game_state.getPacmanPosition()
    food_locations = game_state.getFood().asList()
    distance_2_closest_food = min([manhattanDistance(position, location) for location in food_locations], default = 0.5)
    score = game_state.getScore()

    return score + 1.0 / distance_2_closest_food
    
# Abbreviation
better = betterEvaluationFunction

