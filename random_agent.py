from agent import Agent
import random

# implementation of random-moving agent
class RandomAgent(Agent):

  # possible direction vectors [rowDelta, colDelta]
  DIRS = [[0, 1], [-1, 0], [0, -1], [1, 0]]

  def __init__(self, gridWorld, row, col, char='R'):
    self.row = row
    self.col = col
    self.char = char
    gridWorld.place(self.row, self.col, char)

  # gets new random direction, moves there
  def update(self, gridWorld):
    # take out moves when on edges (ccw)
    moves = self.DIRS.copy()
    if self.col == gridWorld.cols-1:
      moves.remove([0, 1])
    if self.row == 0:
      moves.remove([-1, 0])
    if self.col == 0:
      moves.remove([0, -1])
    if self.row == gridWorld.rows-1:
      moves.remove([1, 0])

    delta = random.choice(moves)
    gridWorld.move(self.row, self.col, self.row+delta[0], self.col+delta[1])
    self.row += delta[0]
    self.col += delta[1]
    return False # no authority to end game