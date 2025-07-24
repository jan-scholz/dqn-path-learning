.PHONY: run build-web run-web clean run-maze

WEBAPP_DIR=src/webapp

clean-all: clean

run:
	hatch run uvicorn dqn_maze.main:app

build-web:
	cd $(WEBAPP_DIR) && npm install && npm run build

run-web:
	cd $(WEBAPP_DIR) && npm run dev 

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf $(WEBAPP_DIR)/dist

clean-all:
	rm -rf $(WEBAPP_DIR)/node_modules

run-maze:
	hatch run python src/dqn_maze/maze_environment.py

