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
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()   
        
        # Influences Pacman to keep distance between ghost and itself 
        for ghost in newGhostStates:
            ghostDist = manhattanDistance(newPos, ghost.getPosition()) 

            if ghostDist > 0:
                score += ghostDist
            
                
        # Influences pacman to decrease the distance between the closest food and itself.
        foodDistances = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        if len(foodDistances):
            score -= min(foodDistances)

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
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
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        def max_agent(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), None)
            
            legalActions = state.getLegalActions(0)
            best_score = -99999
            best_action = None
            for action in legalActions:
                score = min_agent(state.generateSuccessor(0, action), 1, depth)[0]
                if score > best_score:
                    best_score = score
                    best_action = action
                    
            return (best_score, best_action)

        def min_agent(state,ghost, depth):
            if state.isLose() or state.isWin() or depth == self.depth:
                return (self.evaluationFunction(state), None)
            
            legalActions = state.getLegalActions(ghost)
            if len(legalActions) == 0:
                return (self.evaluationFunction(state), None)
            
            best_score = 99999
            score = best_score
            best_action = None


            for action in legalActions:
                if ghost == state.getNumAgents() - 1:
                    score = max_agent(state.generateSuccessor(ghost, action), depth + 1)[0]
                else:
                    score = min_agent(state.generateSuccessor(ghost, action), ghost +1, depth)[0]

                if score < best_score: 
                    best_score = score
                    best_action = action

            return (best_score, best_action)

        return max_agent(gameState, 0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_agent(state, depth, alpha, beta):
            
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), None)

            legalActions = state.getLegalActions(0)
            if len(legalActions) == 0:
                return (self.evaluationFunction(state), None)

            best_score = -99999.0
            score = best_score
            best_action = None
            
            for action in legalActions:
                score = min_agent(state.generateSuccessor(0, action), 1, depth, alpha, beta)[0]
                if (best_score < score):
                    best_score = score
                    best_action = action

                if best_score >= beta:
                    return (best_score, best_action)

                alpha = max(alpha, best_score)

            return (best_score, best_action)

        def min_agent(state, ghost, depth, alpha, beta):
            
            if state.isLose() or state.isWin() or depth == self.depth:
                return (self.evaluationFunction(state), None)

            legalActions = state.getLegalActions(ghost)
            if len(legalActions) == 0:
                return (self.evaluationFunction(state), None)

            best_score = 99999.0
            score = best_score
            best_action = None
            
            for action in legalActions:
                if ghost == state.getNumAgents() - 1:
                    score = max_agent(state.generateSuccessor(ghost, action), depth + 1, alpha, beta)[0]
                else:
                    score = min_agent(state.generateSuccessor(ghost, action), ghost +1, depth, alpha, beta)[0]
            
                if score < best_score:
                    best_score = score
                    best_action = action

                if best_score <= alpha:
                    return (best_score, best_action)
                
                beta = min(beta, best_score)

            return (best_score, best_action)

        alpha = -99999.0
        beta = 99999.0
        return max_agent(gameState, 0, alpha, beta)[1]
    

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
        "*** YOUR CODE HERE ***"
        
        def max_agent(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), None)

            legalActions = state.getLegalActions(0)
            best_score = -99999
            best_action = None
            for action in legalActions:
                score = exp_agent(state.generateSuccessor(0, action), 1, depth)[0]
                if  best_score < score:
                    best_score = score
                    best_action = action

            return (best_score, best_action)
        
        def exp_agent(state, ghost, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), None)

            legalActions = state.getLegalActions(ghost)
            if len(legalActions) == 0:
                return (self.evaluationFunction(state), None)

            best_score = 0
            best_action = None
            score = 0
            for action in legalActions:
                if ghost == state.getNumAgents() - 1:
                    score += max_agent(state.generateSuccessor(ghost, action), depth + 1)[0]
                else:
                    score += exp_agent(state.generateSuccessor(ghost, action), ghost + 1, depth)[0]

                prob = score/len(legalActions)
                best_score += prob
            
            return (best_score, best_action)

        return max_agent(gameState, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

      This evaluation function focuses on minimiziing distance to the closest food pellet 
      while maintaining a safe distance from the ghost by rewarding going towards the pellets
      and discouraging getting close to ghosts. If ghosts are scared, then it is valuable
      to go towards them to eat them. Capsules are not encouraged to go after unless near by.
      Not trying to eat food pellets has a negative affect on score. 
    """
    "*** YOUR CODE HERE ***"
    
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood().asList()
    currCaps = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = currentGameState.getScore()

    if currentGameState.isWin():
        return 99999.0
    if currentGameState.isLose():
        return -99999.0
    
    foodDistances = [manhattanDistance(food, currPos) for food in currFood] 
    
    ghostDistances = [manhattanDistance(currPos, ghost.getPosition()) for ghost in ghostStates if ghostState.scaredTimer == 0]

    if len(ghostDistances) > 0:
        minGhost = min(ghostDistances)
        score += -1.5*(1.0/minGhost)
        
    scaredDistances = [manhattanDistance(currPos, ghost.getPosition()) for ghost in ghostStates if ghostState.scaredTimer > 0]
    
    if len(scaredDistances) > 0:
        minScared =  min(scaredDistances)
        score += -2.0*minScared
    
    score += -2.0*min(foodDistances)
    score += -10.0 * len(currCaps)
    score += -4.0 * len(currFood)


    return score
    
# Abbreviation
better = betterEvaluationFunction

