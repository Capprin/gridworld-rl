from random_agent import RandomAgent
from policy import Policy

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
#           - update value for visited states
#           - update policy based on values
#       - set alpha for ea. training from scratch (multiple games)
#       - either:
#           - run a fixed number of games
#           - run until avg. steps to end are low
#       - save policy


class LearningAgent(RandomAgent):

  MOVE_REWARD = -1
  WIN_REWARD = 30

  def __init__(self, gridWorld, row, col, alpha, v0=None, valuesFile=None, char='L', target='R'):
    # place myself in world
    super(LearningAgent, self).__init__(gridWorld, row, col, char)
    self.target = target

    # initialize values
    if v0 is not None:
      self.values = [[v0]*gridWorld.cols for _ in range(gridWorld.rows)]
    elif valueFile is not None:
      self.load(valuesFile)
    else:
      raise Exception("must specify either v0 or valuesFile")

    # initialize alpha, rewards, policy
    self.alpha = alpha
    self.rewards = {} #dictionary, indexed by lists of [row, col]
    self.policy = Policy(self.values)

  # run every game iteration; updates position according to policy, saves rewards
  def update(self, gridWorld):
    # see if target is adjacent
    for i in range(4):
      # if adjacent, consider ourselves finished
      adjRow = self.row + self.DIRS[i][0]
      adjCol = self.col + self.DIRS[i][1]
      try:
        if adjRow < 0 or adjCol < 0:
          # python doesn't count <0 as OB
          raise
        char = gridWorld.get(adjRow, adjCol)
      except:
        # adjacent is out of bounds, so skip
        continue
      if char == self.target:
        # win; add reward for location
        self.rewards[(adjRow, adjCol)] = self.WIN_REWARD
        return True

    # target not adjacent, so just move (saving reward)
    delta = self.policy.choose(self.row, self.col)
    try:
      gridWorld.move(self.row, self.col, self.row+delta[0], self.col+delta[1])
    except:
      print("Exception while moving from (" + str(self.row) + ", " + str(self.col) + ").")
      print("Moving towards (" + str(delta[0]) + ", " + str(delta[1]) + ")")
      print("Policy at this point is " + str(self.policy.pol[self.row][self.col]))
      raise
    self.row += delta[0]
    self.col += delta[1]
    self.rewards[(self.row, self.col)] = self.MOVE_REWARD
    return False

  # updates stored value according to monte carlo policy evaluation
  def valueUpdate(self, row, col, reward):\
    self.values[row][col] += self.alpha*(reward - self.values[row][col])

  # run value updates, create new policy
  def reset(self, gridWorld, row, col):
    # update values for visited states (locations)
    for loc, rew in self.rewards.items():
      self.valueUpdate(loc[0], loc[1], rew)
    # create new policy
    self.policy = Policy(self.values)
    # reset rewards
    self.rewards = {}
    # move to new location
    gridWorld.place(row, col, self.char)
    gridWorld.place(self.row, self.col, gridWorld.EMPTY)
    self.row = row
    self.col = col

  # saves values
  def save(self, fileName):
    with open(fileName, 'w') as f:
      for row in self.values:
        for val in row:
          f.write(str(val) + ' ')
        f.write('\n')

  # loads values
  def load(self, fileName):
    with open(fileName, 'r') as f:
      self.values = [int(line.split(' ')) for line in f.readlines()]