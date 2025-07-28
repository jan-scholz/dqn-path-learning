# Reinforcement Learning with Deep Q Networks (DQN)

A general framework to apply Q-Learning to path finding. Users can train on an example environment and observe the results.


## Approach

Q-Learning is an off-policy temporal difference (TD) method that learns the optimal action-value function (Q-function) by updating estimates based on both the immediate reward and the maximum estimated future rewards. It does this without requiring a model of the environment. Using deep neural networks to estimate the Q-function is especially advantageous in environments where the number of possible states-action pairs is very large. The hope is that a neural network is able to generalize and provide meaningful outputs even for cases that haven't been seen before (unlike an explicit Q-value table).

## Installation

```bash
python -m venv .venv
. .venv/bin/activate
pip install hatch uv
```

## Run

```bash
make run
```

## Endpoints

```bash
curl -X POST http://localhost:8000/create_maze \
  -H "Content-Type: application/json" \
  -d '{"maze": "S . . X G\n. X . X .\n. . . . .\nX X . X .\n. . . . ."}'
```
