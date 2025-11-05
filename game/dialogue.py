# dialogue.py

level_dialogues = {
    1: [
        "Level 1 complete.",
        "A: \"I can't even pass the tutorial!\"",
        "B: \"That's fine — most people fail at reading the instructions called 'Life.' \"",
        "Press space to proceed to the next level.",
    ],
    2: [
        "Level 2 complete.",
        "A: \"I think I've finally figured out this game, just like my life.\"",
        "B: \"Careful — that's usually when the tutorial ends.\"",
        "Press space to proceed to the next level.",
    ],
    3: [
        "Level 3 complete.",
        "A: \"Every level feels impossible now.\"",
        "B: \"That's how the game tells you, you're getting close to something worth failing for.\"",
        "Press space to proceed to the next level.",
    ],
    4: [
        "Level 4 complete.",
        "A: \"This level keeps repeating similar steps, which makes it feel easier.\"",
        "B: \"Is it possible that you've become stronger?\"",
        "Press space to proceed to the next level.",
    ],
    5: [
        "Level 5 complete.",
        "A: \"I beat the final level… Although it seemed impossible, I did it.\"",
        "B: \"Life requires constant experimentation; nothing is impossible.\"", 
        "...Looking back, it's all just a passing phase.",
        "Press space to view the ending.",
    ],
}

# 当玩家五关都用最短步数时，额外对白:
perfect_dialogue = [
    "Achieve the best number of moves in all levels",
    "A: \"I'm not playing the game, I'm writing a walkthrough.\"",
    "B: \"If you want to show off, saying \'I'm just too lazy to take the extra step\' will sound cooler.\"",
    "Achievement: 【The Optimal Solution in Life】",
    "Press space to end",
]

# 如果不是最短步数全满分，普通结局对白:
normal_dialogue = [
    "Congratulations on clearing the game (without any emotional reaction)",
    "A: \"Walking a few more steps is good exercise.\"",
    "B: \"There are many ways to live life.\"",
    "Thank you for visiting.",
    "Press space to end",
]

