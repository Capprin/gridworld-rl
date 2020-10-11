from random_agent import RandomAgent

# learning overview
#   - known rewards:
#       - (-1) every step in world (ea. location other than target)
#       - (+30) when capture target
#   - state space: ea. location in grid
#   - action space: ea. direction: up, down, left, right
#   - policy: markov chain
#       - ea. state has assoc. probability for next actions (next state)
#           - initially equal probabilities, aka random
#       - prob. of ea. action defined by state "value," V(s)
#           - ea. game, construct policy based on V(s) for adjacent spots
#   - use monte carlo policy eval (first visit) for value
#       - run policy for full "game"
#           - record reward for each visited state
#           - in practice, r(row,col) = reward
#       - update value
#           - V(s) = V(s) + alpha(reward-V(s))
#           - alpha is "tuning" parameter:
#               - 0 prioritizes old information
#               - 1 prioritizes new information
#           - in reality, probably V(row, col)
#   - workflow:
#       - for ea. game:
#           - load policy
#           - run "game," receiving rewards
#           - update value for states
#           - update policy based on values
#       - set alpha for ea. training from scratch (multiple games)
#       - either:
#           - run a fixed number of games
#           - run until avg. steps to end are low
#       - save policy


class LearningAgent(RandomAgent):

  def __init__(self, gridWorld, row, col, char='L', target='R'):
    self.target = target
    super(LearningAgent, self).__init__(gridWorld, row, col, char)

  def update(self, gridWorld):
    # see if target is adjacent
    for i in range(4):
      # if adjacent, consider ourselves finished
      try:
        char = gridWorld.get(self.row+self.DIRS[i][0], self.col+self.DIRS[i][1])
      except:
        # adjacent is out of bounds, so skip
        continue
      if char == self.target:
        return True
    # target not adjacent, so just move
    return super().update(gridWorld)