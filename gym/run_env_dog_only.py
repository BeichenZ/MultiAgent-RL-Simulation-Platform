"""
Found this from morvan's website, to be modified for our environment
Using:
Tensorflow: 1.0
gym: 0.7.3
"""


import gym
import numpy as np
import time
from RL_brain import DeepQNetwork

env = gym.make('sheep-v0')
env = env.unwrapped

print(env.action_space)
print(env.observation_space)


RL = DeepQNetwork(n_actions=env.DISCRETE_Action_Count,
                  n_features=env.FEATURE_Count,
                  learning_rate=0.01, e_greedy=0.9,
                  replace_target_iter=100, memory_size=2000,
                  e_greedy_increment=0.001,)

total_steps = 0
REWARD_DISTANCE = 100000
REWARD_RADIUS= 50



for i_episode in range(1000):

    #reset is not correctly working
    observation = env.reset()
    observation = np.asarray(observation)
    ep_r = 0
    while True:
        env.render()
        #print(observation)
        action = RL.choose_action(observation)

        observation_, reward, done,info = env.step(action=action)

        # CHANGE THE OBSERVATION FROM THE ENVIRONMENT
        DogX, DogY, distance_to_target = observation_

        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        #print('current reward is :',reward)
        if total_steps > 1000:
            RL.learn()

        if done:
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  ' epsilon: ', round(RL.epsilon, 2))
            time.sleep(3)
            break

        observation = np.asarray(observation_)
        total_steps += 1

RL.plot_cost()