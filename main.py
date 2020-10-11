from gridworld import GridWorld
from random_agent import RandomAgent
from learning_agent import LearningAgent
from os import system
from time import sleep

# constants
CLEAR_CMD = 'cls' #for windows, use 'clear' for linux
DRAW_SIM = True #draws sim/delays (for watching, not training)

def tryDraw():
  if DRAW_SIM:
    system(CLEAR_CMD)
    gridWorld.draw()
    sleep(0.5)

# setup
gridWorld = GridWorld()
randomAgent = RandomAgent(gridWorld, 3, 9)
learningAgent = LearningAgent(gridWorld, 2, 4)
tryDraw()

done = False
while not done:
  # let each agent move (done manually)
  # learning agent authoritative for end
  randomAgent.update(gridWorld)
  done = learningAgent.update(gridWorld)

  # optionally, draw grid
  tryDraw()