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
    observation = env._reset()
    observation = np.asarray(observation)
    ep_r = 0
    while True:
        env.render()
        print(observation)
        action = RL.choose_action(observation)

        observation_, reward, done,info = env.step(action=action)

        # CHANGE THE OBSERVATION FROM THE ENVIRONMENT
        # Add the sheep's centroid
        DogX,DogY,SheepCOMX,SheepCOMY,distance_to_sheep_centroid,distance_to_target, ave_distance_to_centroid = observation_

        # check the sheep movement in this step
        sheepMovementX = observation_[2]-observation[2]
        sheepMovementY = observation_[3]-observation[3]
        print('the movement of the sheep: ',sheepMovementX,sheepMovementY)
        # check if the sheep is closer to the final destination
        movement = observation_[5]-observation[5]
        reward = -movement
        print('reward from the movement of the sheep is ', reward)

        # when the com is within a radius to the final destination there is a reward to the dog
        if (distance_to_target <= REWARD_DISTANCE and ave_distance_to_centroid <= REWARD_RADIUS):

            r1 = 1/distance_to_target
            r2 = 1/ave_distance_to_centroid
            reward = reward + r1+r2
        elif (distance_to_target <= REWARD_DISTANCE):
            reward = reward + 1/2*1/(REWARD_DISTANCE - distance_to_target)

        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        print('current reward is :',reward)
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