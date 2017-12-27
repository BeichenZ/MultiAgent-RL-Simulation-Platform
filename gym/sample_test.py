import gym
import threading

e = threading.Event()

env = gym.make('sheep-v0')
env.reset()

while 1:
    env.render()
    env.step(env.action_space.sample())
    #print(env.get_sheep_centroid())
    e.wait(0.005)