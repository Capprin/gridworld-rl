import random

# policy: 
#   - move in adjacent direction of greatest value
class Policy:

  # possible direction vectors [rowDelta, colDelta]
  DIRS = [[0, 1], [-1, 0], [0, -1], [1, 0]]

  def __init__(self, values):
    self.rows = len(values)
    self.cols = len(values[1])
    self.pol = []
    for r in range(self.rows):
      self.pol.append([])
      for c in range(self.cols):
        # get adjacent values, ccw from +cols
        adj = []
        for i in range(4):
          adjRow = r + self.DIRS[i][0]
          adjCol = c + self.DIRS[i][1]
          if adjRow < 0 or adjCol < 0 or adjRow >= self.rows or adjCol >= self.cols:
            # out of bounds
            continue
          if not adj:
            adj = [self.DIRS[i]]
          else:
            stored = values[r + adj[0][0]][c + adj[0][1]]
            if values[adjRow][adjCol] >= stored:
              # current adjacent is equal or greater
              adj.append(self.DIRS[i])
        # save possible directions (of greatest, equal value)
        self.pol[r].append(adj)

  # chooses randomly from possible directions
  def choose(self, row, col):
    return random.choice(self.pol[row][col])
