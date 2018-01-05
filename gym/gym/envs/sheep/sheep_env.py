import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.sheep import rendering
from gym.envs.sheep import SheepGroup
from gym.envs.sheep import DogGroup
from pyglet.window import key
import pdb
import numpy as np
import time

'''
LEGEND
grey dot  = sheep
red dot   = dog
green dot = target
blue dot  = sheep center
'''

class SheepEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  #Env Set-up variable
  SCREEN_WIDTH =1200
  SCREEN_HEIGHT = 700
  TARGET_X = 900
  TARGET_Y = 500
  #finishing radius can be changed later
  FINISH_RADIUS = 100
  SHEEP_RADIUS = 50
  Default_SheepCount = 0
  Default_DogCount = 1
  DISCRETE_Action_Count = 4 #Number of action when discrete number of action spaces is used
  FEATURE_Count = 3
  def __init__(self):
    np.random.seed(int(time.time()))
    self.action_space = spaces.Discrete(self.DISCRETE_Action_Count)
    self.viewer = None

    self.sheepGroup = SheepGroup.SheepGroup( self.Default_SheepCount, self.Default_DogCount,self.SCREEN_WIDTH,self.SCREEN_HEIGHT);
    #Now, the list of dogs technically belongs to sheepGroup
    self.dogGroup = self.sheepGroup
    #self._reset()

    # Need to figure out the high for our case
    high = np.array([np.inf] * 6)
    self.observation_space = spaces.Box(-high, high)
    self._seed()
    return

  def if_done(self):
      #when it done we need to make sure the average radius of the herd is smaller than a fixed radius
      if(self.get_dist_sqr_to_target() <= self.FINISH_RADIUS*self.FINISH_RADIUS):
          return True
      return False
  def get_reward(self):
      #start with sparse award for experiements
      if(self.if_done()):
          return 100
      else:
          return 100*(1060000 - self.get_dist_sqr_to_target())/1060000
  def _step(self, action=None):
    #TO-Do: Implementi Action for Shepherd
    assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
    self.sheepGroup.executeDogAction(action)

    self.sheepGroup.cleanPreviousState()

    #Handle Different Action Space Choice
    #observation consists on distance of centroid to target and average distance of sheeps to centroid
    #assume one dog situation
    allDogLocations=self.sheepGroup.get_DogsLocation()
    #assume the dog can see the centroid location of the sheep
    return [50*int(round(allDogLocations[0][0]/50)), 50*int(round(allDogLocations[0][1]/50)), 0],self.get_reward(),self.if_done(),{}
    #return [50*int(round(allDogLocations[0][0]/50)), 50*int(round(allDogLocations[0][1]/50)), self.get_dist_sqr_to_target()],self.get_reward(),self.if_done(),{}

  def _seed(self, seed=None):
      self.np_random, seed = seeding.np_random(seed)
      return [seed]

  def get_dist_sqr_to_target(self):
      allDogLocations = self.sheepGroup.get_DogsLocation()
      return 50*int(round((self.TARGET_X - allDogLocations[0][0])**2 + (self.TARGET_Y - allDogLocations[0][1])**2)/50)

  def _reset(self):
    # Need to be changed later
    if (self.sheepGroup.SheepList is not None):
        for sheep in self.sheepGroup.SheepList:
            sheep.X = np.random.randint(0, self.SCREEN_WIDTH)
            sheep.Y = np.random.randint(0, self.SCREEN_HEIGHT)
            sheep.velocityX = np.random.random_integers(0, 1000) / 500
            sheep.velocityY = np.random.random_integers(0, 1000) / 500
    if (self.sheepGroup.DogList is not None):
        for dog in self.sheepGroup.DogList:
            dog.X = np.random.randint(0, self.SCREEN_WIDTH)
            dog.Y = np.random.randint(0, self.SCREEN_HEIGHT)
            dog.velocityX = np.random.random_integers(0, 1000) / 500
            dog.velocityY = np.random.random_integers(0, 1000) / 500
    allDogLocations = self.sheepGroup.get_DogsLocation() 
    #return [50*int(round(allDogLocations[0][0]/50)), 50*int(round(allDogLocations[0][1]/50)), self.get_dist_sqr_to_target()]
    return [50*int(round(allDogLocations[0][0]/50)), 50*int(round(allDogLocations[0][1]/50)), 0]

  def key_press(self, symbol, modifier):
      key_moveSize = 30
      if symbol==key.LEFT: 
        self.dogGroup.DogList[0].X -= key_moveSize
        self.dogGroup.DogList[0].velocityX = -key_moveSize
      if symbol==key.RIGHT: 
        self.dogGroup.DogList[0].X += key_moveSize
        self.dogGroup.DogList[0].velocityX = key_moveSize
      if symbol==key.UP: 
        self.dogGroup.DogList[0].Y += key_moveSize
        self.dogGroup.DogList[0].velocityY = key_moveSize
      if symbol==key.DOWN: 
        self.dogGroup.DogList[0].Y -= key_moveSize
        self.dogGroup.DogList[0].velocityY = -key_moveSize
      if symbol==key.A: 
        self.dogGroup.DogList[1].X -= key_moveSize
        self.dogGroup.DogList[0].velocityX = -key_moveSize
      if symbol==key.D: 
        self.dogGroup.DogList[1].X += key_moveSize
        self.dogGroup.DogList[0].velocityX = key_moveSize
      if symbol==key.W: 
        self.dogGroup.DogList[1].Y += key_moveSize
        self.dogGroup.DogList[0].velocityY = key_moveSize
      if symbol==key.S: 
        self.dogGroup.DogList[1].Y -= key_moveSize
        self.dogGroup.DogList[0].velocityY = -key_moveSize

  def _render(self, mode='human', close=False):
    if close:
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
        return

    curSheepList = self.sheepGroup.SheepList
    curDogList = self.dogGroup.DogList
    if self.viewer is None:
        self.viewer = rendering.Viewer(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.viewer.window.on_key_press = self.key_press

        target_translation = rendering.Transform()
        target_circ = rendering.make_circle(10)
        target_circ.set_color(0, 0.7, 0)
        target_circ.add_attr(target_translation)
        self.viewer.add_geom(target_circ)
        target_translation.set_translation(self.TARGET_X, self.TARGET_Y)

        self.sheepTranlations = []
        for sheep in curSheepList:
            translation = rendering.Transform()
            circ = rendering.make_circle(5)
            circ.set_color(0.5, 0.5, 0.5)
            circ.add_attr(translation)
            self.viewer.add_geom(circ)
            self.sheepTranlations.append(translation)
        self.dogTranlations = []
        for dog in curDogList:
            translation = rendering.Transform()
            circ = rendering.make_circle(10)
            circ.set_color(1, 0, 0)
            circ.add_attr(translation)
            self.viewer.add_geom(circ)
            self.dogTranlations.append(translation)

    for ind, translation in enumerate(self.sheepTranlations):
        translation.set_translation(curSheepList[ind].X,curSheepList[ind].Y)
    for ind, translation in enumerate(self.dogTranlations):
        translation.set_translation(curDogList[ind].X, curDogList[ind].Y)
  

    return self.viewer.render(return_rgb_array = mode=='rgb_array')
    