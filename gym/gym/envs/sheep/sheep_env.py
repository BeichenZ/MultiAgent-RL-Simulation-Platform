import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.sheep import rendering
from gym.envs.sheep import SheepGroup
import pdb

class SheepEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  #Env Set-up variable
  screen_width =600
  screen_height = 600
  def __init__(self):
    self.action_space = spaces.Discrete(4)
    self.viewer = None
    #TO-DO: enable # of sheeps as a input parameter
    #TO-DO: make the sheep positions random
    self.sheep_positions = [[50, 100], [267, 234]]

    #To-Do:initialize the group of sheep
    self.sheepGroup = SheepGroup.SheepGroup(sheepCount = 10);
    self.reset()
    return

  def _step(self, action):
  	# use Boids to update sheep positions. Below is just a placeholder
  	# which make them move diagonally
  	#for i in range(len(self.sheep_positions)):
  		#self.sheep_positions[i][0] -= 1
  		#self.sheep_positions[i][1] -= 1
    #TO-Do: Implementi Action for Shepherd
    self.sheepGroup.UpdateLocations();
    return

  def _reset(self):
  	return

  def _render(self, mode='human', close=False):
    if close:
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
        return


    if self.viewer is None:
        self.viewer = rendering.Viewer(self.screen_width, self.screen_height)
        self.circTranlations = []
        for i in range(len(self.sheep_positions)):
            translation = rendering.Transform()
            circ = rendering.make_circle(20)
            circ.set_color(.5, .5, 0.5)
            circ.add_attr(translation)
            self.viewer.add_geom(circ)
            self.circTranlations.append(translation)
        

    for ind, translation in enumerate(self.circTranlations):
    	translation.set_translation(self.sheep_positions[ind][0], self.sheep_positions[ind][1])
    
    return self.viewer.render(return_rgb_array = mode=='rgb_array')
    