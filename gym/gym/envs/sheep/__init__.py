from gym.envs.registration import register
# have to come back and check this

#register the env in /gym/envs/_init_.py:
register(
    id = 'sheepEnv-v0',
    entry_point = 'gym.envs.sheep:sheep_env'
)
#Add the environment to the scoreboard in the /gym/scoreboard/_init_.py:
# add_task(
#     id = 'sheepEnv-v0',
#     summary = "this the environment for reinforcement learning"
#     group = 'sheep simulation',
#     contributor = 'ENPH 1759 group',
# )

from gym.envs.sheep.sheep_env import SheepEnv