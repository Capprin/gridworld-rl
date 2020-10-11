# manages a simple gridworld of characters
class GridWorld:

  EMPTY = '_'

  # creates a matrix filled with EMPTY character
  def __init__(self, rows=5, cols=10):
    self.grid = []
    self.rows = 5
    self.cols = 10
    for row in range(rows):
      row = []
      for col in range(cols):
        row.append(self.EMPTY)
      self.grid.append(row)

  # sets row, col in grid to char
  def place(self, row, col, char):
    self.grid[row][col] = char

  def get(self, row, col):
    return self.grid[row][col]

  # moves contents of fromRow, fromCol to toRow, toCol
  def move(self, fromRow, fromCol, toRow, toCol):
    char = self.grid[fromRow][fromCol]
    self.grid[fromRow][fromCol] = self.EMPTY
    self.grid[toRow][toCol] = char

  # draws grid with axis numbering
  def draw(self):
    # add column numbering
    out = '  ' + ' '.join([str(i) for i in range(len(self.grid[1]))])

    # add newline, row number and space-delimited row contents
    for i in range(len(self.grid)):
      out += '\n' + str(i) + ' ' + ' '.join(self.grid[i])
    print(out)