from gridworld import GridWorld
from random_agent import RandomAgent
from learning_agent import LearningAgent
from os import system
from time import sleep
import matplotlib.pyplot as plt

# constants
ITERATIONS = 100
ALPHA = 0.8
VALUE_INIT = 0
DRAW_SIM = False #draws sim/delays (for watching, not training)
CLEAR_CMD = 'cls' #for windows, use 'clear' for linux

def tryDraw():
  if DRAW_SIM:
    system(CLEAR_CMD)
    gridWorld.draw()
    sleep(0.5)

# setup
gridWorld = GridWorld()
learningAgent = LearningAgent(gridWorld, 2, 4, ALPHA, VALUE_INIT)

# learning iterations
steps = [0] * ITERATIONS
for i in range(ITERATIONS):
  # setup
  randomAgent = RandomAgent(gridWorld, 3, 9)
  tryDraw()

  # play a game
  done = False
  while not done:
    # let each agent move (done manually)
    # learning agent authoritative for end
    randomAgent.update(gridWorld)
    done = learningAgent.update(gridWorld)
    
    # optionally, draw grid
    tryDraw()

    # increment steps
    steps[i] += 1

  # reset agent(triggering learning)
  learningAgent.reset(gridWorld, 2, 4)
  gridWorld.place(randomAgent.row, randomAgent.col, gridWorld.EMPTY)

learningAgent.save("etc/agentValues.txt")
plt.bar(range(ITERATIONS), steps)
plt.ylabel('Steps to goal')
plt.xlabel('Iterations')
plt.show()