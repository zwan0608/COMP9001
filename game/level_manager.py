# level_manager.py
import copy
from settings import TILE_SIZE, BEST_STEPS

class LevelState:
    def __init__(self, walls, goals, boxes, player_pos):
        self.walls = walls
        self.goals = goals
        self.boxes = boxes
        self.player_pos = player_pos

class LevelManager:
    def __init__(self):
        self.current_level_index = 1  # 从1开始到5
        self.state = None
        self.original_state = None
        self.player_steps = 0  # 当前关步数
        self.best_steps = BEST_STEPS

    def load_level(self, level_index: int):
        self.current_level_index = level_index
        walls = []
        goals = []
        boxes = []
        player_pos = None

        path = f"levels/level{level_index}.txt"
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]

        for row_idx, line in enumerate(lines):
            for col_idx, ch in enumerate(line):
                x = col_idx
                y = row_idx

                if ch == '#':
                    walls.append((x,y))
                elif ch == '.':
                    pass  # 只是地板
                elif ch == 'o':
                    goals.append((x,y))
                elif ch == '$':
                    boxes.append((x,y))
                elif ch == '*':  # 箱子在目标点
                    boxes.append((x,y))
                    goals.append((x,y))
                elif ch == '@':
                    player_pos = (x,y)
                elif ch == '+':  # 玩家站在目标点
                    player_pos = (x,y)
                    goals.append((x,y))

        self.state = LevelState(walls, goals, boxes, player_pos)
        self.original_state = copy.deepcopy(self.state)
        self.player_steps = 0

    def reset_level(self):
        self.state = copy.deepcopy(self.original_state)
        self.player_steps = 0

    def is_completed(self):
        # 所有箱子位置都在 goals 里就算过关
        return all(box in self.state.goals for box in self.state.boxes)

    def get_tile_rect(self, grid_x, grid_y):
        return (grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

