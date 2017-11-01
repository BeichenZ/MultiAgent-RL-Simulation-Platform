import gym
from time import sleep
env = gym.make('sheep-v0')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())
    sleep(0.2)
    #env.step(env.action_space.sample()) # take a random action