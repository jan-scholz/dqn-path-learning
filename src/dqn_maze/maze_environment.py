import json

import numpy as np


class Maze:
    def __init__(self):
        self.grid = None
        self.rows, self.cols = 0, 0
        self.action_names = ["up", "down", "left", "right"]
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def _initialize_grid(self, grid_list):
        self.grid = np.array(grid_list)
        self.rows, self.cols = self.grid.shape

        if not np.any(self.grid == "S"):
            raise ValueError("Grid must contain a start position 'S'")
        if not np.any(self.grid == "G"):
            raise ValueError("Grid must contain a start position 'G'")

        self.start = tuple(map(int, np.argwhere(self.grid == "S")[0]))
        self.goal = tuple(map(int, np.argwhere(self.grid == "G")[0]))

    def is_valid_state(self, state):
        row, col = state
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row, col] != "X"
        return False

    def get_next_state(self, state, action_idx):
        row, col = state
        d_row, d_col = self.actions[action_idx]
        next_state = (row + d_row, col + d_col)

        if self.is_valid_state(next_state):
            return next_state
        return state

    def get_reward(self, state, action_idx, next_state):
        if next_state == self.goal:
            return 100
        elif next_state == state:
            return -10
        else:
            return -1

    def from_str(self, maze_str):
        rows = [r.split() for r in maze_str.strip().splitlines()]
        ncols = len(rows[0])
        grid_list = []

        for row in rows:
            if len(row) != ncols:
                raise ValueError(f"Row length {len(row)} != {ncols}")
            grid_list.append(row)

        self.from_list_of_lists(grid_list)

    def from_list_of_lists(self, grid_list):
        self._initialize_grid(grid_list)

    def __str__(self):
        if self.grid is None:
            return "Grid not initialized."
        s = f"Grid ({self.rows}x{self.cols})\n"
        s += "\n".join([" ".join(r) for r in self.grid])
        s += "\n" + f"Start at {self.start} and goal at {self.goal}"
        return s


class QTableAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.env = None
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.state = None
        self.rewards = []
        self.step = None

    def add_environment(self, env):
        # if self.env is None:
        #     raise ValueError("Agent needs to be initialized with proper env.")
        self.env = env
        self._init_q_table()

    def _init_q_table(self):
        self.q_table = np.zeros((self.env.rows, self.env.cols, len(self.env.actions)))
        self.q_table[0, 0, 0] = 1
        self.q_table[1, 0, 0] = 10

    def epsilon_greedy_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(len(self.env.actions))
        else:
            # return the action_idx of the highest value action
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        try:
            max_next_q = np.max(self.q_table[next_state])
        except IndexError:
            print(f"{next_state} is outside q-table of shape {self.q_table.shape}.")

        # Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        current_q = self.q_table[state][action]
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def train(self, episodes=1000):
        episode_rewards = []

        for episode in range(episodes):
            state = self.env.start
            total_reward = 0
            steps = 0
            max_steps = 100  # prevent infinite loops

            while state != self.env.goal and steps < max_steps:
                action = self.epsilon_greedy_action(state)
                next_state = self.env.get_next_state(state, action)
                reward = self.env.get_reward(state, action, next_state)
                self.update_q_value(state, action, reward, next_state)
                state = next_state
                total_reward += reward
                steps += 1

            episode_rewards.append(total_reward)

        return episode_rewards

    def get_policy_idx(self):
        return np.argmax(self.q_table, axis=2)

    def get_policy_name(self):
        policy = self.get_policy_idx()
        return np.array(self.env.action_names)[policy]

    def train_step(self):
        if self.state is None:
            self.state = self.env.start
        if self.step is None:
            self.step = 0
        else:
            self.step += 1

        action = self.epsilon_greedy_action(self.state)
        next_state = self.env.get_next_state(self.state, action)
        reward = self.env.get_reward(self.state, action, next_state)
        self.update_q_value(self.state, action, reward, next_state)
        self.rewards.append(reward)

        params = {
            "step": self.step,
            "state": self.state,
            "next_state": next_state,
            "action": self.env.action_names[action],
            "rewards": self.rewards,
            "rows": self.env.rows,
            "cols": self.env.cols,
            "q_table": self.q_table_to_json(),
        }

        self.state = next_state
        return params

    def q_table_to_json(self):
        result = []
        rows, cols, nactions = self.q_table.shape
        for y in range(rows):
            for x in range(cols):
                cell = {
                    "x": x,
                    "y": y,
                    "values": {
                        action: float(self.q_table[y, x, i])
                        for i, action in enumerate(self.env.action_names)
                    },
                }
                result.append(cell)

        return json.dumps(result)


def main():
    maze_str = """
        S . . X G
        . X . X .
        . . . . .
        X X . X .
        . . . . .
    """

    maze = Maze()
    maze.from_str(maze_str)
    print(maze)
    print()
    # print(maze.get_next_state((0, 0), 1))

    agent = QTableAgent(maze)
    # agent.train(10)

    # print(agent.q_table)
    # print()
    # print(agent.get_policy_idx())
    # print(agent.get_policy_name())

    # print(agent.train_step())
    # print(agent.train_step())


if __name__ == "__main__":
    main()
