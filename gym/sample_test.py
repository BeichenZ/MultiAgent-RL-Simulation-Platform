import gym
import threading

e = threading.Event()

env = gym.make('sheep-v0')
env.reset()

while 1:
    env.render()

    print(str(env.action_space.sample()))
    env.step(env.action_space.sample())

    e.wait(0.005)