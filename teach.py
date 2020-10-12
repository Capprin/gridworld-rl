from gridworld import GridWorld
from random_agent import RandomAgent
from learning_agent import LearningAgent
from os import system
from time import sleep
import plotly.graph_objects as go

# constants
ITERATIONS = 50
ALPHA = 0.9
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

# save values
learningAgent.save("etc/agentValues.txt")

# plot steps vs. iterations
fig1 = go.Figure()
fig1.add_trace(go.Bar(y=steps))
fig1.update_layout(
  title="Steps to Goal over Simulated Iterations",
  xaxis_title="Iterations",
  yaxis_title="Steps"
)

# plot value results (gradient informs direction)
fig2 = go.Figure()
fig2.add_trace(go.Surface(z=learningAgent.values))
fig2.update_layout(
  title="Computed Location Values",
  scene = dict(
    xaxis_title="Column",
    yaxis_title="Row")
)

fig1.show()
fig2.show()