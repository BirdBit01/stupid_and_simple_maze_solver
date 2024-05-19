from PIL import Image, ImageDraw
class Runner:
    def __init__(self, start_tile):
        self.start_tile = start_tile
        self.current_tile = self.start_tile
        self.previous_tiles = []
    
    def get_current_tile(self):
        return self.current_tile
    
    def get_previous_tiles(self):
        return self.previous_tiles
    
    def add_explored_tile(self, tile):
        self.previous_tiles.append(tile)

    def move_tile(self, new_tile):
        self.current_tile = new_tile

class Maze:
    def __init__(self, file):
        self.maze_file = file
        self.create_maze()

    def create_maze(self):
        self.maze = []
        self.start_tile = []
        self.end_tile = []
        with open(self.maze_file, "r") as f:
            for i, line in enumerate(f.readlines()):
                self.maze.append(line.rstrip())
                for j,tile in enumerate(line):
                    if tile == "A":
                        self.start_tile = [i,j]
                    elif tile == "B":
                        self.end_tile = [i,j]

    def get_end(self):
        return self.end_tile
    def get_start(self):
        return self.start_tile
    def get_maze(self):
        return self.maze
    def get_width(self):
        return len(self.maze[0])
    def get_height(self):
        return len(self.maze)

class Search():
    def __init__(self, runner, maze):
        self.runner = runner
        self.maze = maze
    
    def solve(self):
        self.solution_found = False
        self.valid_moves = []
        while not self.solution_found:
            self.possible_moves = [
                ("up", [self.runner.get_current_tile()[0] - 1, self.runner.get_current_tile()[1]]),
                ("down", [self.runner.get_current_tile()[0] + 1, self.runner.get_current_tile()[1]]),
                ("right", [self.runner.get_current_tile()[0], self.runner.get_current_tile()[1] + 1]),
                ("left", [self.runner.get_current_tile()[0], self.runner.get_current_tile()[1] - 1]),
            ]


            for p_move in self.possible_moves:
                if p_move[1][0] >= len(self.maze.get_maze()) or p_move[1][1] >= len(self.maze.get_maze()):
                    continue
                elif self.maze.get_maze()[p_move[1][0]][p_move[1][1]] in (" ", "A", "B"):
                    if self.maze.get_maze()[p_move[1][0]][p_move[1][1]] == "B":
                        self.solution_found = True
                        self.valid_moves.append([p_move[1][0], p_move[1][1]])
                        print("Solution found")
                    elif [p_move[1][0], p_move[1][1]] not in self.runner.get_previous_tiles(): 
                        self.valid_moves.append([p_move[1][0], p_move[1][1]])

            self.runner.add_explored_tile(self.runner.get_current_tile())
            if self.valid_moves:
                self.runner.move_tile(self.valid_moves[0])
                self.valid_moves.pop(0)

    def get_solution(self):
        return self.runner.get_previous_tiles()
    
    def draw_solution(self):
        cell_size = 10
        img = Image.new("RGBA", (self.maze.get_width() * cell_size, self.maze.get_height() * cell_size), "black")
        draw = ImageDraw.Draw(img)

        for i in range(self.maze.get_height()):
            for j in range(self.maze.get_width()):
                color = (0,0,0)
                if [i,j] in self.runner.get_previous_tiles():
                    color = (255, 255, 0)
                if self.maze.get_maze()[i][j] == "A":
                    color = (0, 255, 0)
                if self.maze.get_maze()[i][j] == "B":
                    color = (255, 0, 0)
                if self.maze.get_maze()[i][j] == "w":
                    color = (128, 128, 128)


                draw.rectangle((cell_size * j, cell_size * i, cell_size * (j+1), cell_size * (i+1)), fill=color)

        img.save("solution.png")

m = Maze("maze3.txt")
r = Runner(m.get_start())
s = Search(r,m)
s.solve()
print(s.get_solution())
s.draw_solution()

