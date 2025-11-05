# player.py
import pygame

MOVE_KEYS = {
    pygame.K_UP:    (0, -1),
    pygame.K_w:     (0, -1),
    pygame.K_DOWN:  (0, 1),
    pygame.K_s:     (0, 1),
    pygame.K_LEFT:  (-1, 0),
    pygame.K_a:     (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d:     (1, 0),
}

class PlayerController:
    def __init__(self, level_manager):
        self.lvl = level_manager  # 引用 LevelManager

    def try_move(self, key):
        if key not in MOVE_KEYS:
            return

        dx, dy = MOVE_KEYS[key]

        px, py = self.lvl.state.player_pos
        target = (px + dx, py + dy)

        # 1. 目标格是墙？ -> 不动
        if target in self.lvl.state.walls:
            return

        # 2. 目标格是箱子？
        if target in self.lvl.state.boxes:
            box_target = (target[0] + dx, target[1] + dy)

            # 2.1 箱子后面是墙 or 其他箱子 -> 推不动
            if (box_target in self.lvl.state.walls) or (box_target in self.lvl.state.boxes):
                return

            # 2.2 可以推，更新箱子位置
            #    从盒子列表中移除旧位置，加上新位置
            self.lvl.state.boxes.remove(target)
            self.lvl.state.boxes.append(box_target)

            # 玩家前进到target
            self.lvl.state.player_pos = target
            self.lvl.player_steps += 1
            return

        # 3. 目标格是空地/目标点 -> 允许走
        self.lvl.state.player_pos = target
        self.lvl.player_steps += 1

