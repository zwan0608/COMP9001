# settings.py

TILE_SIZE = 64  # 单个格子的像素大小，记得把图片也做成这个大小比较方便
PIC_SIZE = 65

FPS = 60

LEVEL_COUNT = 5

# 每一关的最短步数（你需要自己填真实的最优步数）
BEST_STEPS = {
    1: 23,
    2: 51,
    3: 17,
    4: 56,
    5: 60,
}

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UI_BG = (0, 0, 0)
UI_TEXT = (255, 255, 255)

SCREEN_BG = (30, 30, 30)  # 背景底色

