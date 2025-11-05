# main.py

import pygame
import sys
import os

from settings import *
from assets import Assets
from level_manager import LevelManager
from player import PlayerController
from dialogue import level_dialogues, perfect_dialogue, normal_dialogue


# =========================
# 字体安全加载
# =========================
def safe_font(path, size):
    """
    安全加载字体：
    - 如果对应的 .ttf 文件存在，就使用它
    - 否则回退到 pygame 自带的默认字体
    """
    if os.path.exists(path):
        return pygame.font.Font(path, size)
    else:
        print(f"[Warning] Can't find font:{path}, I'll use what I have.")
        return pygame.font.SysFont(None, size)


# =========================
# 绘制关卡画面 & UI
# =========================
def draw_level(screen, assets, lvl, ui_font):
    # 整个背景先填成黑色
    screen.fill((0, 0, 0))

    # ---------- 1. 计算地图范围与像素尺寸 ----------
    all_cells = (
        lvl.state.walls
        + lvl.state.goals
        + lvl.state.boxes
        + [lvl.state.player_pos]
    )
    # 安全保护：如果没有内容直接返回
    if not all_cells:
        return

    max_x = max(x for x, y in all_cells)
    max_y = max(y for x, y in all_cells)

    # 地图像素宽高（多加1是因为坐标是从0开始计格子）
    map_pixel_w = (max_x + 1) * TILE_SIZE
    map_pixel_h = (max_y + 1) * TILE_SIZE

    # ---------- 2. 确定地图放在屏幕哪里 ----------
    # 我们把地图放在屏幕中央 (不包含右侧UI区域)
    # 屏幕右侧预留一个UI栏，比如 250px 宽
    UI_PANEL_W = 250
    screen_w, screen_h = screen.get_size()

    play_area_w = screen_w - UI_PANEL_W  # 地图可占用的最大宽度
    play_area_h = screen_h

    offset_x = (play_area_w - map_pixel_w) // 2
    offset_y = (play_area_h - map_pixel_h) // 2

    # ---------- 3. 先画floor+goal，再画墙/箱子/玩家 ----------
    # 先把所有可见地板都画出来
    # 我们迭代 0..max_x, 0..max_y，这样格子就严密对齐
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            draw_x = offset_x + x * TILE_SIZE
            draw_y = offset_y + y * TILE_SIZE

            # 地板
            screen.blit(assets.floor, (draw_x, draw_y))

            # 如果这个格子是目标点，也叠目标贴图
            if (x, y) in lvl.state.goals:
                screen.blit(assets.goal, (draw_x, draw_y))

    # 墙
    for (x, y) in lvl.state.walls:
        draw_x = offset_x + x * TILE_SIZE
        draw_y = offset_y + y * TILE_SIZE
        screen.blit(assets.wall, (draw_x, draw_y))

    # 箱子
    for (x, y) in lvl.state.boxes:
        draw_x = offset_x + x * TILE_SIZE
        draw_y = offset_y + y * TILE_SIZE
        if (x, y) in lvl.state.goals:
            screen.blit(assets.box_on_goal, (draw_x, draw_y))
        else:
            screen.blit(assets.box, (draw_x, draw_y))

    # 玩家
    px, py = lvl.state.player_pos
    player_x = offset_x + px * TILE_SIZE
    player_y = offset_y + py * TILE_SIZE
    screen.blit(assets.player, (player_x, player_y))

    # ---------- 4. 右侧UI面板 ----------
    # 画一个侧边栏背景
    panel_rect = pygame.Rect(play_area_w, 0, UI_PANEL_W, screen_h)
    pygame.draw.rect(screen, (20, 20, 20), panel_rect)

    # 在右侧面板里显示信息（步数，最佳步数，当前关卡号等）
    steps_text = f"Steps: {lvl.player_steps}"
    best_text = f"Best: {lvl.best_steps[lvl.current_level_index]}"
    level_text = f"Level: {lvl.current_level_index}"
    reset_text = "R = restart"
    goal_text = "Push all boxes onto targets."

    text_surfs = [
        ui_font.render(level_text, True, (255,255,255)),
        ui_font.render(steps_text, True, (255,255,255)),
        ui_font.render(best_text, True, (255,255,255)),
        ui_font.render(reset_text, True, (200,200,200)),
        ui_font.render(goal_text, True, (200,200,200)),
    ]

    # 把这些文字竖着排在侧边栏
    panel_x = play_area_w + 20
    panel_y = 20
    line_gap = 40
    for surf in text_surfs:
        screen.blit(surf, (panel_x, panel_y))
        panel_y += line_gap



# =========================
# 对白遮罩层绘制
# =========================
def draw_dialogue_overlay(screen, alt_font, lines):
    """
    关卡结束对白界面
    使用 alt_font 字体，添加文字阴影效果
    """
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    screen.blit(overlay, (0, 0))

    y_start = 100
    line_gap = 45
    shadow_offset = (2, 2)  # 阴影偏移（x,y），可改成(3,3)更明显

    for line in lines:
        # 渲染阴影层（黑色）
        shadow_surf = alt_font.render(line, True, (0, 0, 0))
        surf = alt_font.render(line, True, (255, 128, 0))

        # 居中位置计算
        x = (screen.get_width() - surf.get_width()) // 2
        y = y_start

        # 先绘制阴影（稍微往右下角偏移）
        screen.blit(shadow_surf, (x + shadow_offset[0], y + shadow_offset[1]))

        # 再绘制文字本体
        screen.blit(surf, (x, y))

        y_start += line_gap





# =========================
# 最终结局对白绘制
# =========================
def draw_ending(screen, dialogue_font, achievement_font, lines):
    """
    结局对白界面：
    - 默认对白字体 dialogue_font
    - 特殊行（含《 或 Achievement: 开头的行）使用 achievement_font
    """
    screen.fill((0, 0, 0))
    y_start = 100
    line_gap = 50  # 行距

    for line in lines:
        # 判断是否是特殊行（你也可以用别的条件，比如包含 "《"）
        if "《" in line or "Achievement" in line:
            shadow = achievement_font.render(line, True, (0,0,0))
            surf = achievement_font.render(line, True, (255, 215, 0))  # 金色文字
        else:
            shadow = dialogue_font.render(line, True, (0,0,0))
            surf = dialogue_font.render(line, True, (255,255,255))
        screen.blit(shadow, (62, y_start + 2))
        screen.blit(surf, (60, y_start))
        y_start += line_gap



# =========================
# 文字自动换行工具
# =========================
def draw_wrapped_text(surface, text_lines, font, color, x, y, max_width, line_height):
    """
    将 text_lines 里的每一行根据 max_width 自动分成多行并绘制到 surface 上。
    返回绘制结束后的 y 位置，方便后续继续往下画别的内容。
    """
    for line in text_lines:
        words = line.split(" ")
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > max_width:
                # 当前行塞不下了，先把 current_line 画出来，换到下一行
                surface.blit(font.render(current_line, True, color), (x, y))
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line
        # 把最后残余的一行画出来
        if current_line:
            surface.blit(font.render(current_line, True, color), (x, y))
            y += line_height
    return y


# =========================
# Intro 界面绘制
# =========================
def draw_intro(screen, title_font, subtitle_font, author_font, body_font, assets):
    """
    Intro 界面：
    - 不同字体/字号分别用于标题、副标题、署名、正文说明
    - 正文支持自动换行
    """
    screen.fill((0, 0, 0))

    # 标题区文本
    title_surf = title_font.render("Box Pushing Game", True, (255, 215, 0))
    subtitle_surf = subtitle_font.render("—— Basic How To Play ——", True, (20,140,240))
    author_surf = author_font.render("Created by Wang – 9001", True, (180, 180, 180))

    # 说明正文（你给的版本）
    lines = [
        "Use the arrow keys or W/A/S/D to move your character.",
        "If there's empty space behind a box, you can push it.",
        "Objective: Push all the boxes to the target point.",
        "Press R to restart (steps will be reset to zero).",
        "The top will display your step count and the minimum number of steps required for this level.",
        "After completing a level, a dialogue will appear. Press space to proceed to the next level.",
        "Try to complete all levels with the fewest steps possible.",
        "The levels progress from easy to difficult, or at least that's how it appears(lol).",
        "Press space to start the game.",
    ]

    # 绘制标题、副标题、作者
    screen.blit(title_surf, (100, 60))
    screen.blit(subtitle_surf, (100, 120))
    screen.blit(author_surf, (100, 160))

    # 正文多行自动换行
    x_start = 100
    y_start = 220
    max_width = screen.get_width() - 150  # 右边预留空白，避免超出屏幕
    line_height = 34  # 行距（可以根据 body_font 大小微调）

    draw_wrapped_text(
        surface=screen,
        text_lines=lines,
        font=body_font,
        color=(127,255,0),
        x=x_start,
        y=y_start,
        max_width=max_width,
        line_height=line_height
    )

        # 绘制右上角主题图
    if hasattr(assets, "theme") and assets.theme:
        img = assets.theme
        # 距离顶部 40 像素，右边留 40 像素
        x = screen.get_width() - img.get_width() - 40
        y = 40
        screen.blit(img, (x, y))


# =========================
# 主函数
# =========================
def main():
    pygame.init()
    clock = pygame.time.Clock()

    # --------------- 窗口大小 ---------------
    # 如果 intro 文本还是太长掉出屏幕，可把高度调高一些，比如 800。
    SCREEN_W = 1000
    SCREEN_H = 700
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    pygame.display.set_caption("Box Pushing Demo")

    # --------------- 字体加载 ---------------
    # 你可以把 fonts/title.ttf 等换成你实际的字体文件名
    title_font = safe_font("fonts/title.ttf", 56)        # 大标题
    subtitle_font = safe_font("fonts/subtitle.ttf", 32)  # 副标题（更小）
    author_font = safe_font("fonts/author.ttf", 24)      # 作者名（最小）
    body_font = safe_font("fonts/dialogue.ttf", 28)      # 正文/对白主字体
    achievement_font = safe_font("fonts/achievement.ttf", 36)
    dialogue_alt_font = safe_font("fonts/dialogue_alt.ttf", 30)
    ui_font = body_font                                  # UI用同一套也可以
    dialogue_font = body_font                            # 对话框/结局对白也用它

    # --------------- 游戏资源与管理对象 ---------------
    assets = Assets()
    lvl = LevelManager()
    player_controller = PlayerController(lvl)

    # perfect_flags[i] == True 表示第 i 关是按最优步数通关
    perfect_flags = {i + 1: False for i in range(LEVEL_COUNT)}

    # 游戏状态机
    # "intro"    : 说明界面
    # "playing"  : 游戏中
    # "dialogue" : 单关结束对白
    # "ending"   : 全部关卡之后的结局对白
    # "quit"     : 准备退出
    game_mode = "intro"

    # 当前对白（dialogue模式 和 ending模式 都会用到）
    current_dialogue_lines = []

    # 注意：现在不在这里预先载入 level1，等 intro 按空格后再载入
    # lvl.load_level(1)  # <-- 不在这里做

    while game_mode != "quit":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_mode = "quit"

            elif event.type == pygame.KEYDOWN:
                # INTRO：按空格开始游戏，加载第1关
                if game_mode == "intro":
                    if event.key == pygame.K_SPACE:
                        lvl.load_level(1)
                        game_mode = "playing"

                # PLAYING：移动/推箱子/重置关卡
                elif game_mode == "playing":
                    if event.key == pygame.K_r:
                        lvl.reset_level()
                    else:
                        before_steps = lvl.player_steps
                        player_controller.try_move(event.key)
                        after_steps = lvl.player_steps

                        # 是否过关？
                        if lvl.is_completed():
                            best = lvl.best_steps[lvl.current_level_index]
                            perfect_flags[lvl.current_level_index] = (after_steps == best)

                            # 加载这一关的对白
                            current_dialogue_lines = level_dialogues[lvl.current_level_index]
                            game_mode = "dialogue"

                # DIALOGUE：显示关卡对白，按空格进入下一关或结局
                elif game_mode == "dialogue":
                    if event.key == pygame.K_SPACE:
                        if lvl.current_level_index < LEVEL_COUNT:
                            next_level = lvl.current_level_index + 1
                            lvl.load_level(next_level)
                            game_mode = "playing"
                        else:
                            # 全部关打完，生成结局对白
                            if all(perfect_flags[i + 1] for i in range(LEVEL_COUNT)):
                                current_dialogue_lines = perfect_dialogue
                            else:
                                current_dialogue_lines = normal_dialogue
                            game_mode = "ending"

                # ENDING：按空格退出
                elif game_mode == "ending":
                    if event.key == pygame.K_SPACE:
                        game_mode = "quit"

        # ======================
        # 绘制阶段
        # ======================
        if game_mode == "intro":
            draw_intro(screen, title_font, subtitle_font, author_font, body_font, assets)

        elif game_mode == "playing":
            draw_level(screen, assets, lvl, ui_font)

        elif game_mode == "dialogue":
            draw_level(screen, assets, lvl, ui_font)
            draw_dialogue_overlay(screen, dialogue_alt_font, current_dialogue_lines)


        elif game_mode == "ending":
            # 纯黑背景 + 结局对白
            draw_ending(screen, dialogue_font, achievement_font, current_dialogue_lines)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

