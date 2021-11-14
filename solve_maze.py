import numpy as np
from mazelab import BaseMaze
from mazelab import Object
from mazelab import DeepMindColor as color
from mazelab import BaseEnv
from mazelab import VonNeumannMotion

import gym
from gym.spaces import Box
from gym.spaces import Discrete


def solve_maze(x):
    # x = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #  [2, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    #  [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    #  [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
    #  [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    #  [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 3],
    #  [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    #  [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    #  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    #  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    start_idx = np.argwhere(x == 2)
    goal_idx = np.argwhere(x == 3)

    x[start_idx[0][0]][start_idx[0][1]] = 0
    x[goal_idx[0][0]][goal_idx[0][1]] = 0

    env_id = 'Maze-v0'

    class Env(BaseEnv):
        def __init__(self):
            super().__init__()

            self.maze = Maze()
            self.motions = VonNeumannMotion()

            self.observation_space = Box(low=0, high=len(self.maze.objects), shape=self.maze.size, dtype=np.uint8)
            self.action_space = Discrete(len(self.motions))

        def step(self, action):
            motion = self.motions[action]
            current_position = self.maze.objects.agent.positions[0]
            new_position = [current_position[0] + motion[0], current_position[1] + motion[1]]
            valid = self._is_valid(new_position)
            if valid:
                self.maze.objects.agent.positions = [new_position]

            if self._is_goal(new_position):
                reward = +1
                done = True
            elif not valid:
                reward = -1
                done = False
            else:
                reward = -0.01
                done = False
            return self.maze.to_value(), reward, done, {}

        def reset(self):
            self.maze.objects.agent.positions = start_idx
            self.maze.objects.goal.positions = goal_idx
            return self.maze.to_value()

        def _is_valid(self, position):
            nonnegative = position[0] >= 0 and position[1] >= 0
            within_edge = position[0] < self.maze.size[0] and position[1] < self.maze.size[1]
            passable = not self.maze.to_impassable()[position[0]][position[1]]
            return nonnegative and within_edge and passable

        def _is_goal(self, position):
            out = False
            for pos in self.maze.objects.goal.positions:
                if position[0] == pos[0] and position[1] == pos[1]:
                    out = True
                    break
            return out

        def get_image(self):
            return self.maze.to_rgb()

    class Maze(BaseMaze):
        @property
        def size(self):
            return x.shape

        def make_objects(self):
            free = Object('free', 0, color.free, False, np.stack(np.where(x == 0), axis=1))
            obstacle = Object('obstacle', 1, color.obstacle, True, np.stack(np.where(x == 1), axis=1))
            agent = Object('agent', 2, color.agent, False, [])
            goal = Object('goal', 3, color.goal, False, [])
            return free, obstacle, agent, goal

    gym.envs.register(id=env_id, entry_point=Env, max_episode_steps=200)

    import matplotlib.pyplot as plt

    env = gym.make(env_id)
    env.reset()
    # img = env.render('rgb_array')
    # plt.imshow(img)

    from mazelab.solvers import dijkstra_solver

    impassable_array = env.unwrapped.maze.to_impassable()
    motions = env.unwrapped.motions
    start = env.unwrapped.maze.objects.agent.positions[0]
    goal = env.unwrapped.maze.objects.goal.positions[0]
    actions = dijkstra_solver(impassable_array, motions, start, goal)

    return actions
    # print(actions)
