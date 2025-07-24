.PHONY: run clean

run:
	hatch run python src/dqn_maze/maze_environment.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
