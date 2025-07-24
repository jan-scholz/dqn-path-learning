import numpy as np


class Maze:
    def __init__(self):
        self.grid = None

    def _initialize_grid(self, grid_list):
        self.grid = np.array(grid_list)
        self.rows, self.cols = self.grid.shape

        if not np.any(self.grid == "S"):
            raise ValueError("Grid must contain a start position 'S'")
        if not np.any(self.grid == "G"):
            raise ValueError("Grid must contain a start position 'G'")

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
        s = f"Grid ({self.rows}x{self.cols})\n"
        s += "\n".join([" ".join(r) for r in self.grid])
        return s


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


if __name__ == "__main__":
    main()
