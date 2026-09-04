# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
from pacman import GameState
import util
import heapq

from game import Agent

def scoreEvaluationFunction(currentGameState: GameState) -> float:
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return better(currentGameState)
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction: function[float] = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState) -> Directions:
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        _value, action = self.minimaxValue(gameState, 0, 0)
        return action

    def minimaxValue(self, state: GameState, depth, agentIndex) -> tuple[float, Directions]:
        totalAgents = state.getNumAgents()
        if agentIndex >= totalAgents:
            agentIndex = 0
            depth += 1

        hasReachedMaxDepth = depth >= self.depth
        isGameLose = state.isLose()
        isGameWin = state.isWin()
        isTerminalState = hasReachedMaxDepth or isGameLose or isGameWin
        if isTerminalState:
            return self.evaluationFunction(state), None
        
        isMax = agentIndex == 0 # agent is Pacman
        if isMax:
            return self.maxValue(state, depth, agentIndex)
        else:
            return self.minValue(state, depth, agentIndex)

    def maxValue(self, state: GameState, depth, agentIndex):
        bestValue = float("-inf")
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.minimaxValue(successor, depth, agentIndex + 1)
            if successorValue >= bestValue:
                bestValue = successorValue
                bestAction = action
        return bestValue, bestAction
    
    def minValue(self, state: GameState, depth, agentIndex):
        bestValue = float("inf")
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.minimaxValue(successor, depth, agentIndex + 1)
            if successorValue <= bestValue:
                bestValue = successorValue
                bestAction = action
        return bestValue, bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState) -> Directions:
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        _value, action = self.minimaxValue(gameState, 0, 0)
        return action

    def minimaxValue(self, state: GameState, depth, agentIndex, alpha = float("-inf"), beta = float("inf")) -> tuple[float, Directions]:
        totalAgents = state.getNumAgents()
        if agentIndex >= totalAgents:
            agentIndex = 0
            depth += 1

        hasReachedMaxDepth = depth >= self.depth
        isGameLose = state.isLose()
        isGameWin = state.isWin()
        isTerminalState = hasReachedMaxDepth or isGameLose or isGameWin
        if isTerminalState:
            return self.evaluationFunction(state), None
        
        isMax = agentIndex == 0 # agent is Pacman
        if isMax:
            return self.maxValue(state, depth, agentIndex, alpha, beta)
        else:
            return self.minValue(state, depth, agentIndex, alpha, beta)

    def maxValue(self, state: GameState, depth, agentIndex, alpha, beta):
        bestValue = float("-inf")
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.minimaxValue(successor, depth, agentIndex + 1, alpha, beta)
            if successorValue >= bestValue:
                bestValue = successorValue
                bestAction = action
            if bestValue > beta:
                return bestValue, bestAction
            alpha = max(alpha, bestValue)
        return bestValue, bestAction
    
    def minValue(self, state: GameState, depth, agentIndex, alpha, beta):
        bestValue = float("inf")
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.minimaxValue(successor, depth, agentIndex + 1, alpha, beta)
            if successorValue <= bestValue:
                bestValue = successorValue
                bestAction = action
            if bestValue < alpha:
                return bestValue, bestAction
            beta = min(beta, bestValue)
        return bestValue, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        _value, action = self.expectimaxValue(gameState, 0, 0)
        return action

    def expectimaxValue(self, state: GameState, depth, agentIndex) -> tuple[float, Directions]:
        totalAgents = state.getNumAgents()
        if agentIndex >= totalAgents:
            agentIndex = 0
            depth += 1

        hasReachedMaxDepth = depth >= self.depth
        isGameLose = state.isLose()
        isGameWin = state.isWin()
        isTerminalState = hasReachedMaxDepth or isGameLose or isGameWin
        if isTerminalState:
            return self.evaluationFunction(state), None
        
        isMax = agentIndex == 0 # agent is Pacman
        if isMax:
            return self.maxValue(state, depth, agentIndex)
        else:
            return self.expValue(state, depth, agentIndex)

    def maxValue(self, state: GameState, depth, agentIndex):
        bestValue = float("-inf")
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.expectimaxValue(successor, depth, agentIndex + 1)
            if successorValue >= bestValue:
                bestValue = successorValue
                bestAction = action
        return bestValue, bestAction
    
    def expValue(self, state: GameState, depth, agentIndex):
        bestValue = 0
        bestAction = None
        legalActions = state.getLegalActions(agentIndex)
        probability = 1 / len(legalActions)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            successorValue, _successorAction = self.expectimaxValue(successor, depth, agentIndex + 1)
            bestValue += probability * successorValue 
        return bestValue, bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
        - Removes points for each remaining Food
        - Removes points for each remaining Capsules
        - Removes points by how far Pacman is to the nearest Food or Capsule
        - Removes or adds additional points on lose/win
        - Adds points by how close the Ghost is to the Capsules and how close Pacman is to that Ghost

    We try to incentive the Pacman to get all the foods and avoid bad movement behavior by removing points
    for each food and capsule remaining, removing points by how far away Pacman is to the nearest food or capsule,
    adding points by how close the Ghost is to a capsule and how close Pacman is to that Ghost.
    We also add additional points on Win and remove additional points on Lose to balance the Win/Lose bonus/penalty.
    """
    weights = {
        "PACMAN_DISTANCE_TO_FOOD": 5,
        "REMAINING_FOOD": 50,
        "REMAINING_CAPSULES": 50,
        "WIN": 250,
        "LOSE": 250,
        "EATING_GHOST": 500
    }

    configs = {
        "PACMAN_DISTANCE_TO_CAPSULE": 2,
        "GHOST_DISTANCE_TO_CAPSULE": 3,
    }

    score = currentGameState.getScore()
    foodGrid = currentGameState.getFood()
    capsulesList = currentGameState.getCapsules()
    pacmanPosition = currentGameState.getPacmanPosition()
    pacmanDistanceToFood, _targetPosition = calculateNearestPathTo(pacmanPosition, currentGameState, lambda x, y : foodGrid[x][y] == True or (x, y) in capsulesList)

    remainingCapsulesCount = len(capsulesList)
    remainingFoodCount = currentGameState.getNumFood()

    ghostPositions = currentGameState.getGhostPositions()
    for position in ghostPositions:
        ghostDistanceToCapsule, targetCapsulePosition = calculateNearestPathTo(position, currentGameState, lambda x, y : (x, y) in capsulesList)
        pacmanDistanceToCapsuleNearTheGhost, _targetPosition = calculateNearestPathTo(pacmanPosition, currentGameState, lambda x, y : (x, y) == targetCapsulePosition)

        HUNDRED_PERCENT = 1
        ghostDistanceToCapsuleInfluencePercentage = min(HUNDRED_PERCENT, 1 / (max(configs["GHOST_DISTANCE_TO_CAPSULE"], ghostDistanceToCapsule) - configs["GHOST_DISTANCE_TO_CAPSULE"] + 1) ** 2)
        ghostDistanceToPacmanInfluencePercentage = min(HUNDRED_PERCENT, 1 / (max(configs["PACMAN_DISTANCE_TO_CAPSULE"], pacmanDistanceToCapsuleNearTheGhost) - configs["PACMAN_DISTANCE_TO_CAPSULE"] + 1) ** 2)

        hasRemainingCapsules = remainingCapsulesCount > 0

        score += weights["EATING_GHOST"] * ghostDistanceToCapsuleInfluencePercentage * ghostDistanceToPacmanInfluencePercentage * hasRemainingCapsules

    score -= remainingFoodCount * weights["REMAINING_FOOD"]
    score -= remainingCapsulesCount * weights["REMAINING_CAPSULES"]    
    score -= pacmanDistanceToFood * weights["PACMAN_DISTANCE_TO_FOOD"]
    score -= weights["LOSE"] * currentGameState.isLose()
    score += weights["WIN"] * currentGameState.isWin()
    return score

def calculateNearestPathTo(agentPosition, gameState: GameState, isEndTarget) -> tuple[int, tuple[int, int]]:
    wallGrid = gameState.getWalls()

    queue = [(0, int(agentPosition[0]), int(agentPosition[1]))]
    costs = { (int(agentPosition[0]), int(agentPosition[1])): 0 }

    while queue:
        currentCost, x, y = heapq.heappop(queue)

        if isEndTarget(x, y):
            return currentCost, (x, y)

        isMoreExpensiveThanOtherPathAlreadyExplored = currentCost > costs.get((x, y), float("inf"))
        if isMoreExpensiveThanOtherPathAlreadyExplored:
            continue

        actions = (
            (1, 0), # Directions.EAST
            (-1, 0), # Directions.WEST
            (0, 1), # Directions.NORTH
            (0, -1) # Directions.SOUTH
        )

        for dx, dy in actions:
            ax, ay = x + dx, y + dy

            isXInbounds = 0 < ax < wallGrid.width
            isYInbounds = 0 < ay < wallGrid.height
            if isXInbounds and isYInbounds:
                isCoordAWall = wallGrid[ax][ay] == True
                if isCoordAWall:
                    continue
                nextCost = currentCost + 1
                if nextCost < costs.get((ax, ay), float("inf")):
                    costs[(ax, ay)] = nextCost
                    heapq.heappush(queue, (nextCost, ax, ay))
    return -1, (-1, -1)

# Abbreviation
better = betterEvaluationFunction
