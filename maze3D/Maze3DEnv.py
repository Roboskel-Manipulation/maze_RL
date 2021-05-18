import random
import time
# import maze3D.rewards
import rewards
from maze3D.gameObjects import *
from maze3D.assets import *
from maze3D.utils import get_distance_from_goal, checkTerminal
from rl_models.utils import get_config
from maze3D.config import layout_up_right, layout_down_right, layout_up_left

layouts = [layout_down_right, layout_up_left, layout_up_right]

class ActionSpace:
    def __init__(self):
        # self.actions = list(range(0, 14 + 1))
        # self.shape = 1
        self.actions = list(range(0, 3))
        self.shape = 2
        self.actions_number = len(self.actions)
        self.high = self.actions[-1]
        self.low = self.actions[0]

    def sample(self):
        # return [random.sample([0, 1, 2], 1), random.sample([0, 1, 2], 1)]
        return np.random.randint(self.low, self.high + 1, 2)


class Maze3D:
    def __init__(self, config=None,  config_file=None):
        # choose randomly one starting point for the ball
        self.config = get_config(config_file) if config_file is not None else config
        current_layout = random.choice(layouts)
        self.discrete_input = self.config['game']['discrete']
        self.board = GameBoard(current_layout, self.discrete_input)
        self.keys = {pg.K_UP: 1, pg.K_DOWN: 2, pg.K_LEFT: 4, pg.K_RIGHT: 8}
        self.keys_fotis = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 2, pg.K_RIGHT: 3}
        self.running = True
        self.done = False
        self.observation = self.get_state()  # must init board fisrt
        self.action_space = ActionSpace()
        self.observation_shape = (len(self.observation),)
        self.dt = None
        self.fps = 60
        self.reward_type = self.config['SAC']['reward_function'] if 'SAC' in self.config.keys() else None
        self.goal_reward = self.config['SAC']['goal_reward'] if 'SAC' in self.config.keys() else None
        self.state_reward = self.config['SAC']['state_reward'] if 'SAC' in self.config.keys() else None
        rewards.main(self.config)

    def stepOld(self, action, timedout, goal, reset, action_duration=None):
        tmp_time = time.time()
        while (time.time() - tmp_time) < action_duration and not self.done:
            self.board.handleKeys(action)
            self.board.update()
            glClearDepth(1000.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.board.draw()
            pg.display.flip()

            self.dt = clock.tick(self.fps)
            fps = clock.get_fps()
            pg.display.set_caption("Running at " + str(int(fps)) + " fps")
            self.observation = self.get_state()
            if checkTerminal(self.board.ball, goal) or timedout:
                time.sleep(3)
                self.done = True
            if reset:
                timeStart = time.time()
                i=0
                while time.time() - timeStart <= 5:
                    self.board.update()
                    glClearDepth(1000.0)
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    self.board.draw(mode=True, idx=i)
                    pg.display.flip()
                    time.sleep(1)
                    i+=1
        # reward = self.reward_function_maze(timedout, goal=goal)
        reward = rewards.reward_function_maze(self.done, timedout, goal=goal)
        return self.observation, reward, self.done

    def stepNew(self, action, timedout, goal, reset):
        if not reset:
            self.board.handleKeys(action)
            self.board.update()
            glClearDepth(1000.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.board.draw()
            pg.display.flip()

            self.dt = clock.tick(self.fps)
            fps = clock.get_fps()
            pg.display.set_caption("Running at " + str(int(fps)) + " fps")
            self.observation = self.get_state()
        if reset:
            timeStart = time.time()
            i=0
            self.board.update()
            while time.time() - timeStart <= 5:
                glClearDepth(1000.0)
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                self.board.draw(mode=1, idx=i)
                pg.display.flip()
                time.sleep(1)
                i+=1
        goal_reached = checkTerminal(self.board.ball, goal)
        # print(timedout)
        if goal_reached or timedout:
            timeStart = time.time()
            i=0
            self.board.update()
            while time.time() - timeStart <= 3:
                glClearDepth(1000.0)
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                if goal_reached:
                    self.board.draw(mode=2, idx=i)
                else:
                    self.board.draw(mode=3, idx=i)
                pg.display.flip()
                time.sleep(1)
                i+=1

            # time.sleep(5)
            self.done = True
        reward = rewards.reward_function_maze(self.done, timedout, goal=goal)
        # reward = self.reward_function_maze(timedout, goal=goal)
        return self.observation, reward, self.done

    def get_state(self):
        # [ball pos x | ball pos y | ball vel x | ball vel y|  theta(x) | phi(y) |  theta_dot(x) | phi_dot(y) | ]
        return np.asarray(
            [self.board.ball.x, self.board.ball.y, self.board.ball.velocity[0], self.board.ball.velocity[1],
             self.board.rot_x, self.board.rot_y, self.board.velocity[0], self.board.velocity[1]])

    def reset(self):
        self.__init__(config=self.config)
        return self.observation

    def reward_function_maze(self, timedout, goal=None):
    	if self.reward_type == "Sparse" or self.reward_type == "sparse":
    		return self.reward_function_sparse(timedout)
    	elif self.reward_type == "Dense" or self.reward_type == "dense":
    		return self.reward_function_dense(timedout, goal=goal)
    	elif self.reward_type == "Sparse_2" or self.reward_type == "sparse_2":
    		return self.reward_function_sparse2(timedout)

    def reward_function_sparse(self, timedout):
    	# For every timestep -1
    	# Timed out -50
    	# Reach goal +100
    	if self.done and not timedout:
    		return self.goal_reward
    	if timedout:
    		return -50
    	return self.state_reward

    def reward_function_sparse2(self, timedout):
    	# For every timestep -1
    	# Reach goal +100
    	if self.done and not timedout:
    		return self.goal_reward
    	return self.state_reward

    def reward_function_dense(self, timedout, goal=None):
    	# For every timestep -target_distance
    	# Timed out -50
    	# Reach goal +goal_reward
    	if self.done:
    		return self.goal_reward
    	if timedout:
    		return -50
    	# return -target_distance/10 for each time step
    	target_distance = get_distance_from_goal(self.board.ball, goal)
    	return -target_distance / 10

    def reward_function(self, timedout, goal=None):
    	if self.done:
    		return self.goal_reward
    	# Construct here the mathematical reward function
    	# The reward function can depend on time, the distance of 
    	# the ball to the goal, it can be static or anything else
    	# Default is static
    	return -1