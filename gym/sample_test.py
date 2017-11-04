import gym
from time import sleep
import threading

e = threading.Event()


env = gym.make('sheep-v0')
env.reset()

#for _ in range(1000):
x = 1
while x:
    env.render()
    env.step(env.action_space.sample())
    e.wait(0.2)
    #env.step(env.action_space.sample()) # take a random action