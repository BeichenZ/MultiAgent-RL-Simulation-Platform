import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.sheep import rendering
from gym.envs.sheep import SheepGroup
from gym.envs.sheep import DogGroup
from pyglet.window import key
import pdb

class SheepEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  #Env Set-up variable
  SCREEN_WIDTH =1200
  SCREEN_HEIGHT = 700
  Default_SheepCount = 10
  def __init__(self):
    self.action_space = spaces.Discrete(4)
    self.viewer = None

    self.sheepGroup = SheepGroup.SheepGroup( self.Default_SheepCount ,self.SCREEN_WIDTH,self.SCREEN_HEIGHT);

    self.dogGroup = DogGroup.DogGroup(self.SCREEN_WIDTH,self.SCREEN_HEIGHT);
    self.reset()
    return

  def _step(self, action=None):
    #TO-Do: Implementi Action for Shepherd
    self.sheepGroup.updateLocations()
    return

  def _reset(self):
    return

  def key_press(self, symbol, modifier):
      if symbol==key.LEFT: 
        self.dogGroup.DogList[0].X -= 10
      if symbol==key.RIGHT: 
        self.dogGroup.DogList[0].X += 10
      if symbol==key.UP: 
        self.dogGroup.DogList[0].Y += 10
      if symbol==key.DOWN: 
        self.dogGroup.DogList[0].Y -= 10
      if symbol==key.A: 
        self.dogGroup.DogList[1].X -= 10
      if symbol==key.D: 
        self.dogGroup.DogList[1].X += 10
      if symbol==key.W: 
        self.dogGroup.DogList[1].Y += 10
      if symbol==key.S: 
        self.dogGroup.DogList[1].Y -= 10

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
    